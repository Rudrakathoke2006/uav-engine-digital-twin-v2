"""
AeroTwin-PX: 3D MALE-UAV & Aero Piston Engine Digital Twin Visualization
Provides interactive 3D WebGL rendering with Three.js, attitude pitch/roll/yaw orientation,
RPM-driven propeller spinning, subsystem thermal/diagnostic heatmaps, 11 interactive 3D sensor markers,
Raycaster tooltips, camera view modes (Reset, UAV, Engine, Cutaway, Diagnostic), and WebGL fallback protection.
"""

import base64
import json
import os
import streamlit as st
import streamlit.components.v1 as components

# Load MQ-9 Reaper UAV Drone GLB Model
_MODEL_PATH = os.path.join(os.path.dirname(__file__), "assets", "models", "drone.glb")
if not os.path.exists(_MODEL_PATH):
    _MODEL_PATH = os.path.join(os.path.dirname(__file__), "mq-9_reaper_uav_drone.glb")

with open(_MODEL_PATH, "rb") as _f:
    _MODEL_BASE64 = base64.b64encode(_f.read()).decode("utf-8")

def render_3d_digital_twin(twin_state: dict, height: int = 620):
    """
    Renders the interactive 3D MALE-UAV & Engine Digital Twin component.
    """
    state_json = json.dumps(twin_state)
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ margin: 0; padding: 0; overflow: hidden; background-color: #080c14; font-family: 'Segoe UI', sans-serif; }}
            #canvas-container {{ width: 100vw; height: {height}px; position: relative; }}
            
            /* Overlay Controls UI */
            .twin-controls {{
                position: absolute;
                top: 12px;
                left: 12px;
                z-index: 100;
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
            }}
            .twin-btn {{
                background: rgba(30, 41, 59, 0.85);
                border: 1px solid #334155;
                color: #38bdf8;
                padding: 6px 14px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                backdrop-filter: blur(4px);
            }}
            .twin-btn:hover {{
                background: #0284c7;
                color: #ffffff;
                border-color: #38bdf8;
                box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
            }}
            .twin-btn.active {{
                background: #0284c7;
                color: #ffffff;
            }}
            
            /* HUD Data Box */
            .hud-box {{
                position: absolute;
                bottom: 12px;
                left: 12px;
                z-index: 100;
                background: rgba(15, 23, 42, 0.88);
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px 16px;
                color: #e2e8f0;
                font-size: 11px;
                line-height: 1.55;
                backdrop-filter: blur(4px);
                max-width: 340px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            }}
            .hud-title {{ color: #38bdf8; font-weight: bold; margin-bottom: 4px; border-bottom: 1px solid #334155; padding-bottom: 2px; display: flex; justify-content: space-between; }}
            .hud-val {{ color: #10b981; font-weight: bold; }}
            .hud-warn {{ color: #ef4444; font-weight: bold; }}
            
            /* Sensor Tooltip Overlay */
            #sensor-tooltip {{
                position: absolute;
                display: none;
                z-index: 200;
                background: rgba(15, 23, 42, 0.95);
                border: 1px solid #38bdf8;
                border-radius: 8px;
                padding: 10px 14px;
                color: #ffffff;
                font-size: 11px;
                line-height: 1.5;
                pointer-events: none;
                box-shadow: 0 4px 16px rgba(0,0,0,0.7);
                backdrop-filter: blur(6px);
                min-width: 180px;
            }}
            .tt-header {{ color: #38bdf8; font-weight: bold; border-bottom: 1px solid #334155; padding-bottom: 3px; margin-bottom: 4px; }}
            .tt-row {{ display: flex; justify-content: space-between; gap: 12px; }}
            .tt-val {{ color: #10b981; font-weight: bold; }}
            .tt-res {{ color: #f59e0b; font-weight: bold; }}
            
            /* WebGL Fallback */
            #webgl-fallback {{
                display: none;
                position: absolute;
                top: 0; left: 0; width: 100%; height: 100%;
                background: #0f172a;
                color: #ef4444;
                text-align: center;
                padding-top: 150px;
                font-size: 16px;
            }}
        </style>
        
        <!-- Load Three.js & OrbitControls & GLTFLoader -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
    </head>
    <body>
        <div id="canvas-container">
            <div class="twin-controls">
                <button class="twin-btn active" id="btn-uav" onclick="setViewMode('uav')">✈️ UAV VIEW</button>
                <button class="twin-btn" id="btn-engine" onclick="setViewMode('engine')">🔧 ENGINE VIEW</button>
                <button class="twin-btn" id="btn-cutaway" onclick="setViewMode('cutaway')">⚙️ CUTAWAY MODE</button>
                <button class="twin-btn" id="btn-diagnostic" onclick="setViewMode('diagnostic')">🌡️ DIAGNOSTIC VIEW</button>
                <button class="twin-btn" id="btn-reset" onclick="resetCamera()">🔄 RESET VIEW</button>
            </div>
            
            <div class="hud-box" id="hud-box">
                <div class="hud-title"><span>🛸 DIGITAL TWIN 3D HUD</span><span id="hud-mode-tag" style="color:#eab308; font-size:10px;">UAV</span></div>
                <div>Status: <span id="hud-status" class="hud-val">NOMINAL</span> | EHI: <span id="hud-ehi" class="hud-val">95%</span></div>
                <div>Propeller Speed: <span id="hud-rpm" class="hud-val">0 RPM</span></div>
                <div>Engine CHT: <span id="hud-cht">0 °C</span> | EGT: <span id="hud-egt">0 °C</span></div>
                <div>Attitude: P:<span id="hud-pitch">0°</span> R:<span id="hud-roll">0°</span> Y:<span id="hud-yaw">0°</span></div>
                <div>Active Fault: <span id="hud-fault" style="color:#f59e0b;">None</span></div>
                <div>Twin Confidence: <span id="hud-conf" class="hud-val">95%</span></div>
                <div style="font-size:9px; color:#64748b; margin-top:6px; border-top:1px solid #334155; padding-top:4px;">MQ-9 Reaper UAV Drone by Chenzoss, CC Attribution 4.0, via Sketchfab</div>
            </div>
            
            <div id="sensor-tooltip"></div>
            <div id="webgl-fallback">
                <h3>⚠️ DIGITAL TWIN 3D VIEW UNAVAILABLE</h3>
                <p>WebGL is disabled or unsupported on this graphics accelerator.</p>
                <p>Fallback 2D Telemetry & Diagnostics Active.</p>
            </div>
        </div>

        <script>
            // Base64 Embedded MQ-9 Reaper GLB Model Data
            const modelBase64 = "{_MODEL_BASE64}";

            // Parse Unified Twin Visualization State
            const state = {state_json};
            const sensorDetails = state.sensor_details || {{}};
            
            // WebGL Support Check
            function checkWebGL() {{
                try {{
                    const canvas = document.createElement('canvas');
                    return !!(window.WebGLRenderingContext && (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
                }} catch (e) {{ return false; }}
            }}

            if (!checkWebGL()) {{
                document.getElementById('webgl-fallback').style.display = 'block';
            }} else {{
                initThreeScene();
            }}

            let scene, camera, renderer, controls;
            let uavGroup, engineGroup, propellerMesh, cowlingLeft, cowlingRight;
            let cylinderMeshes = [], injectorMeshes = [], oilMesh, exhaustMesh;
            let sensorMarkers = [];
            let raycaster, mouse;
            let currentViewMode = 'uav';
            let cutawayProgress = 0.0;
            let targetCutaway = 0.0;
            
            function initThreeScene() {{
                const container = document.getElementById('canvas-container');
                const width = container.clientWidth;
                const height = container.clientHeight;

                // 1. Scene Setup
                scene = new THREE.Scene();
                scene.background = new THREE.Color(0x080c14);
                scene.fog = new THREE.FogExp2(0x080c14, 0.007);

                // 2. Camera Setup
                camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
                camera.position.set(12, 8, 15);

                // 3. Renderer Setup
                renderer = new THREE.WebGLRenderer({{ antialias: true }});
                renderer.setSize(width, height);
                renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
                renderer.shadowMap.enabled = true;
                container.appendChild(renderer.domElement);

                // 4. OrbitControls
                controls = new THREE.OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;
                controls.dampingFactor = 0.05;
                controls.maxPolarAngle = Math.PI / 2 + 0.1;

                // 5. Lighting
                const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
                scene.add(ambientLight);

                const dirLight = new THREE.DirectionalLight(0xffffff, 1.5);
                dirLight.position.set(20, 40, 20);
                scene.add(dirLight);

                const pointLight = new THREE.PointLight(0x10b981, 1.5, 30);
                pointLight.position.set(0, 2, -2);
                scene.add(pointLight);

                // 6. Grid Floor & Grid Ring
                const gridHelper = new THREE.GridHelper(100, 50, 0x1e293b, 0x0f172a);
                gridHelper.position.y = -4;
                scene.add(gridHelper);

                // 7. Build MQ-9 Reaper UAV & Sensor Markers
                buildUAVModel();
                buildFlightPath();

                // 8. Setup Raycasting & Tooltip Handlers
                raycaster = new THREE.Raycaster();
                mouse = new THREE.Vector2();
                renderer.domElement.addEventListener('mousemove', onMouseMove);
                window.addEventListener('resize', onWindowResize);
                
                // Update HUD Overlay
                updateHUD();

                // Animation Loop
                animate();
            }}

            function buildUAVModel() {{
                uavGroup = new THREE.Group();

                // Fast Native Base64 ArrayBuffer decoding via fetch
                fetch("data:application/octet-stream;base64," + modelBase64)
                    .then(res => res.arrayBuffer())
                    .then(buffer => {{
                        const loader = new THREE.GLTFLoader();
                        loader.parse(buffer, '', function(gltf) {{
                            const model = gltf.scene;
                            model.scale.set(8.5, 8.5, 8.5);
                            model.rotation.set(0, Math.PI, 0);
                            model.position.set(0, 0, 0);
                            
                            model.traverse(function(child) {{
                                if (child.isMesh) {{
                                    child.castShadow = true;
                                    child.receiveShadow = true;
                                }}
                            }});
                            
                            uavGroup.add(model);
                        }}, function(err) {{
                            console.error("GLTF Parse Error:", err);
                        }});
                    }})
                    .catch(err => console.error("GLTF Fetch Error:", err));

                // Add 11 Sensor Markers
                addSensorMarkers();

                scene.add(uavGroup);
            }}

            function addSensorMarkers() {{
                const sensors = [
                    {{ id: 'RPM', key: 'RPM', pos: [0, 0.45, 3.6] }},
                    {{ id: 'CHT', key: 'CHT', pos: [0.85, 0.5, 2.3] }},
                    {{ id: 'EGT', key: 'EGT', pos: [0.0, -0.35, 2.8] }},
                    {{ id: 'OilP', key: 'OilP', pos: [-0.4, -0.5, 2.4] }},
                    {{ id: 'OilT', key: 'OilT', pos: [0.4, -0.5, 2.4] }},
                    {{ id: 'Fuel', key: 'Fuel', pos: [0.0, 0.75, 2.5] }},
                    {{ id: 'Vib', key: 'Vib', pos: [0.0, 0.2, 2.0] }},
                    {{ id: 'Volt', key: 'Volt', pos: [-1.2, 0.1, 0.5] }},
                    {{ id: 'Alt', key: 'Alt', pos: [1.2, 0.1, 0.5] }},
                    {{ id: 'Inj', key: 'Inj', pos: [0.0, 0.5, 3.1] }},
                    {{ id: 'MAP', key: 'MAP', pos: [0.0, -0.2, 1.8] }}
                ];

                sensors.forEach(s => {{
                    const dt = sensorDetails[s.key] || {{ label: s.id, actual: 0, expected: 0, residual: 0, unit: '', health: 95 }};
                    const sphereGeo = new THREE.SphereGeometry(0.12, 12, 12);
                    const isSuspect = dt.health < 80 || Math.abs(dt.residual) > 10;
                    const matColor = isSuspect ? 0xef4444 : 0x38bdf8;
                    const sphereMat = new THREE.MeshBasicMaterial({{ color: matColor, wireframe: true }});
                    
                    const marker = new THREE.Mesh(sphereGeo, sphereMat);
                    marker.position.set(s.pos[0], s.pos[1], s.pos[2]);
                    marker.userData = {{
                        id: s.id,
                        label: dt.label || s.id,
                        actual: dt.actual,
                        expected: dt.expected,
                        residual: dt.residual,
                        unit: dt.unit,
                        health: dt.health
                    }};
                    uavGroup.add(marker);
                    sensorMarkers.push(marker);
                }});
            }}

            function buildFlightPath() {{
                const points = [];
                for (let i = -30; i <= 30; i += 2) {{
                    points.push(new THREE.Vector3(i * 0.8, Math.sin(i * 0.2) * 1.5 - 2, -i * 1.2));
                }}
                const curve = new THREE.CatmullRomCurve3(points);
                const pathGeo = new THREE.BufferGeometry().setFromPoints(curve.getPoints(100));
                const pathMat = new THREE.LineDashedMaterial({{ color: 0x38bdf8, dashSize: 0.5, gapSize: 0.2 }});
                const pathLine = new THREE.Line(pathGeo, pathMat);
                pathLine.computeLineDistances();
                scene.add(pathLine);
            }}

            function setViewMode(mode) {{
                currentViewMode = mode;
                document.querySelectorAll('.twin-btn').forEach(b => b.classList.remove('active'));
                
                if (mode === 'uav') {{
                    document.getElementById('btn-uav').classList.add('active');
                    document.getElementById('hud-mode-tag').innerText = 'UAV';
                    targetCutaway = 0.0;
                    animateCameraTo(new THREE.Vector3(12, 8, 15), new THREE.Vector3(0, 0, 0));
                }} else if (mode === 'engine') {{
                    document.getElementById('btn-engine').classList.add('active');
                    document.getElementById('hud-mode-tag').innerText = 'ENGINE';
                    targetCutaway = 0.0;
                    animateCameraTo(new THREE.Vector3(0.5, 2.2, -5.5), new THREE.Vector3(0, 0.2, -1.0));
                }} else if (mode === 'cutaway') {{
                    document.getElementById('btn-cutaway').classList.add('active');
                    document.getElementById('hud-mode-tag').innerText = 'CUTAWAY';
                    targetCutaway = 1.0;
                    animateCameraTo(new THREE.Vector3(3.8, 2.5, -2.5), new THREE.Vector3(0, 0.2, -0.8));
                }} else if (mode === 'diagnostic') {{
                    document.getElementById('btn-diagnostic').classList.add('active');
                    document.getElementById('hud-mode-tag').innerText = 'HEATMAP';
                    targetCutaway = 0.5;
                    animateCameraTo(new THREE.Vector3(0, 8.5, 0.5), new THREE.Vector3(0, 0, 0));
                }}
            }}

            function resetCamera() {{
                setViewMode('uav');
            }}

            function animateCameraTo(targetPos, targetLookAt) {{
                const startPos = camera.position.clone();
                const startLookAt = controls.target.clone();
                let progress = 0;

                function stepCam() {{
                    progress += 0.06;
                    camera.position.lerpVectors(startPos, targetPos, progress);
                    controls.target.lerpVectors(startLookAt, targetLookAt, progress);
                    controls.update();

                    if (progress < 1.0) {{
                        requestAnimationFrame(stepCam);
                    }}
                }}
                stepCam();
            }}

            function onMouseMove(event) {{
                const rect = renderer.domElement.getBoundingClientRect();
                mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
                mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

                raycaster.setFromCamera(mouse, camera);
                const intersects = raycaster.intersectObjects(sensorMarkers);

                const tooltip = document.getElementById('sensor-tooltip');
                if (intersects.length > 0) {{
                    const marker = intersects[0].object;
                    const d = marker.userData;
                    
                    tooltip.style.display = 'block';
                    tooltip.style.left = (event.clientX - rect.left + 15) + 'px';
                    tooltip.style.top = (event.clientY - rect.top - 15) + 'px';
                    
                    const resSign = d.residual >= 0 ? '+' : '';
                    tooltip.innerHTML = `
                        <div class="tt-header">📡 ${{d.label}}</div>
                        <div class="tt-row"><span>Actual:</span> <span class="tt-val">${{d.actual}} ${{d.unit}}</span></div>
                        <div class="tt-row"><span>Expected:</span> <span>${{d.expected}} ${{d.unit}}</span></div>
                        <div class="tt-row"><span>Residual (ΔS):</span> <span class="tt-res">${{resSign}}${{d.residual}} ${{d.unit}}</span></div>
                        <div class="tt-row"><span>Health Score:</span> <span style="color:#10b981;">${{d.health}}%</span></div>
                    `;
                }} else {{
                    tooltip.style.display = 'none';
                }}
            }}

            function updateHUD() {{
                document.getElementById('hud-status').innerText = state.health_status || 'HEALTHY';
                document.getElementById('hud-ehi').innerText = (state.overall_ehi || 95) + '%';
                document.getElementById('hud-rpm').innerText = (state.rpm || 0) + ' RPM';
                document.getElementById('hud-cht').innerText = (state.cht_c || 0) + ' °C';
                document.getElementById('hud-egt').innerText = (state.egt_c || 0) + ' °C';
                document.getElementById('hud-pitch').innerText = (state.pitch_deg || 0) + '°';
                document.getElementById('hud-roll').innerText = (state.roll_deg || 0) + '°';
                document.getElementById('hud-yaw').innerText = (state.yaw_deg || 0) + '°';
                document.getElementById('hud-fault').innerText = state.predicted_fault || 'None';
                document.getElementById('hud-conf').innerText = (state.digital_twin_confidence || 95) + '%';
            }}

            function animate() {{
                requestAnimationFrame(animate);

                // 1. Smooth Cutaway Cowling Shift Animation
                cutawayProgress += (targetCutaway - cutawayProgress) * 0.1;
                if (cowlingLeft && cowlingRight) {{
                    cowlingLeft.position.x = -0.35 - (cutawayProgress * 0.8);
                    cowlingRight.position.x = 0.35 + (cutawayProgress * 0.8);
                    cowlingLeft.material.opacity = 0.95 - (cutawayProgress * 0.5);
                    cowlingRight.material.opacity = 0.95 - (cutawayProgress * 0.5);
                }}

                // 2. Rotate Propeller based on actual telemetry RPM
                if (propellerMesh && state.rpm) {{
                    const rotSpeed = (state.rpm / 60.0) * 0.15;
                    propellerMesh.rotation.z += rotSpeed;
                }}

                // 3. Apply Aircraft Pitch, Roll, Yaw attitude
                if (uavGroup) {{
                    uavGroup.rotation.x = THREE.MathUtils.degToRad(state.pitch_deg || 0);
                    uavGroup.rotation.z = THREE.MathUtils.degToRad(-state.roll_deg || 0);
                    
                    // Altitude vertical scaling in scene
                    const altY = ((state.altitude_ft || 10000) - 10000) / 4000.0;
                    uavGroup.position.y = Math.max(-2, Math.min(altY, 4));
                }}

                // 4. Thermal & Diagnostic Subsystem Coloring & Visual Fault Localizer
                const faultStr = (state.predicted_fault || '').toLowerCase();
                const chtVal = state.cht_c || 150;
                
                if (cylinderMeshes.length > 0) {{
                    cylinderMeshes.forEach(c => {{
                        if (chtVal > 190 || faultStr.includes('overheating') || faultStr.includes('misfire')) {{
                            c.material.color.setHex(0xef4444); // Red Thermal Overheating
                            c.material.emissive.setHex(0x991b1b);
                        }} else if (chtVal > 170) {{
                            c.material.color.setHex(0xf59e0b); // Amber Thermal Warning
                        }} else {{
                            c.material.color.setHex(0x64748b); // Normal Slate
                            c.material.emissive.setHex(0x000000);
                        }}
                    }});
                }}

                if (injectorMeshes.length > 0) {{
                    injectorMeshes.forEach(inj => {{
                        if (faultStr.includes('injector') || faultStr.includes('coking')) {{
                            inj.material.color.setHex(0xef4444);
                            inj.material.emissive.setHex(0xef4444);
                        }} else {{
                            inj.material.color.setHex(0x0284c7);
                            inj.material.emissive.setHex(0x0284c7);
                        }}
                    }});
                }}

                if (oilMesh) {{
                    if (faultStr.includes('lubrication') || faultStr.includes('oil')) {{
                        oilMesh.material.color.setHex(0xef4444);
                        oilMesh.material.emissive.setHex(0xef4444);
                    }} else {{
                        oilMesh.material.color.setHex(0x16a34a);
                        oilMesh.material.emissive.setHex(0x16a34a);
                    }}
                }}

                if (exhaustMesh) {{
                    const egtVal = state.egt_c || 650;
                    if (egtVal > 780 || faultStr.includes('combustion')) {{
                        exhaustMesh.material.color.setHex(0xef4444);
                        exhaustMesh.material.emissive.setHex(0xd97706);
                    }} else {{
                        exhaustMesh.material.color.setHex(0xeab308);
                        exhaustMesh.material.emissive.setHex(0x000000);
                    }}
                }}

                controls.update();
                renderer.render(scene, camera);
            }}

            function onWindowResize() {{
                const container = document.getElementById('canvas-container');
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }}
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=height)


def render_3d_background_canvas(twin_state: dict, height: int = 400):
    """
    Renders an animated 3D WebGL Drone & Tactical Terrain Grid Canvas.
    """
    state_json = json.dumps(twin_state)
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ margin: 0; padding: 0; overflow: hidden; background-color: #060913; font-family: 'Orbitron', 'Segoe UI', sans-serif; }}
            #bg-canvas-container {{ width: 100vw; height: {height}px; position: relative; }}
            
            .bg-hud-overlay {{
                position: absolute;
                top: 15px;
                left: 18px;
                z-index: 10;
                color: #00f0ff;
                font-family: 'Orbitron', monospace;
                font-size: 11px;
                letter-spacing: 1.5px;
                background: rgba(6, 12, 24, 0.85);
                border: 1px solid rgba(0, 240, 255, 0.3);
                padding: 10px 16px;
                border-radius: 6px;
                backdrop-filter: blur(8px);
                box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
            }}
            .bg-hud-overlay span {{ color: #00ff9d; font-weight: bold; }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
    </head>
    <body>
        <div id="bg-canvas-container">
            <div class="bg-hud-overlay">
                <div>✈️ 3D MALE UAV DRONE VIRTUAL REPLICA | ALT: <span>{twin_state.get('altitude_ft', 18000)} FT</span> | RPM: <span>{twin_state.get('rpm', 4800)}</span> | EHI: <span>{twin_state.get('engine_health_index', 96.8)}%</span></div>
                <div style="font-size:9px; color:#64748b; margin-top:3px; font-family:'Segoe UI',sans-serif;">MQ-9 Reaper UAV Drone by Chenzoss, CC Attribution 4.0, via Sketchfab</div>
            </div>
        </div>

        <script>
            const modelBase64 = "{_MODEL_BASE64}";
            const state = {state_json};
            const container = document.getElementById('bg-canvas-container');
            
            const scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x060913, 0.015);
            
            const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.set(0, 8, 22);
            
            const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
            container.appendChild(renderer.domElement);
            
            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.autoRotate = true;
            controls.autoRotateSpeed = 1.2;
            
            // Ambient & Point Lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 1.2);
            scene.add(ambientLight);
            
            const cyanLight = new THREE.PointLight(0x00f0ff, 2, 50);
            cyanLight.position.set(10, 15, 10);
            scene.add(cyanLight);
            
            const emeraldLight = new THREE.PointLight(0x00ff9d, 2, 50);
            emeraldLight.position.set(-10, -5, -10);
            scene.add(emeraldLight);

            // 1. 3D Tactical Wireframe Grid Floor
            const gridHelper = new THREE.GridHelper(100, 40, 0x00f0ff, 0x0f2744);
            gridHelper.position.y = -6;
            scene.add(gridHelper);

            // 2. 3D Particle Starfield
            const particleCount = 400;
            const geometry = new THREE.BufferGeometry();
            const positions = new Float32Array(particleCount * 3);
            for(let i=0; i<particleCount*3; i++) {{
                positions[i] = (Math.random() - 0.5) * 80;
            }}
            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            const particleMaterial = new THREE.PointsMaterial({{ color: 0x00f0ff, size: 0.25, transparent: true, opacity: 0.7 }});
            const particles = new THREE.Points(geometry, particleMaterial);
            scene.add(particles);

            // 3. 3D MALE UAV Drone Model Mesh Group
            const droneGroup = new THREE.Group();
            let prop;
            
            fetch("data:application/octet-stream;base64," + modelBase64)
                .then(res => res.arrayBuffer())
                .then(buffer => {{
                    const loader = new THREE.GLTFLoader();
                    loader.parse(buffer, '', function(gltf) {{
                        const model = gltf.scene;
                        model.scale.set(8.5, 8.5, 8.5);
                        model.rotation.set(0, Math.PI, 0);
                        model.position.set(0, 0, 0);
                        
                        model.traverse(function(child) {{
                            if (child.isMesh) {{
                                child.castShadow = true;
                                child.receiveShadow = true;
                            }}
                        }});
                        
                        droneGroup.add(model);
                    }}, function(err) {{
                        console.error("GLTF Background Parse Error:", err);
                    }});
                }})
                .catch(err => console.error("GLTF Background Fetch Error:", err));

            scene.add(droneGroup);

            // Animation Loop
            let clock = new THREE.Clock();
            function animate() {{
                requestAnimationFrame(animate);
                const time = clock.getElapsedTime();
                
                // Propeller Spin if available
                if (prop) {{
                    const rpm = state.rpm || 4800;
                    prop.rotation.z += (rpm / 60) * 0.05;
                }}
                
                // Ambient Drone Altitude Floating Motion
                droneGroup.position.y = Math.sin(time * 1.5) * 0.4;
                droneGroup.rotation.z = Math.sin(time * 1.2) * 0.05;
                droneGroup.rotation.x = Math.cos(time * 0.9) * 0.04;
                
                particles.rotation.y = time * 0.02;
                gridHelper.position.z = (time * 2) % 2.5;

                controls.update();
                renderer.render(scene, camera);
            }}
            animate();

            window.addEventListener('resize', () => {{
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=height)

