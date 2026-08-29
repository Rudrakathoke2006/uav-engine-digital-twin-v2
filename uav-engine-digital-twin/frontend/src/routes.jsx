import React from "react";
import { createBrowserRouter } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import LiveMonitoringPage from "./pages/LiveMonitoringPage";
import DigitalTwinPage from "./pages/DigitalTwinPage";
import PredictiveHealthPage from "./pages/PredictiveHealthPage";
import MissionSimulatorPage from "./pages/MissionSimulatorPage";
import AlertsPage from "./pages/AlertsPage";
import MissionHistoryPage from "./pages/MissionHistoryPage";
import MissionReplayPage from "./pages/MissionReplayPage";

export const router = createBrowserRouter([
  { path: "/", element: <LoginPage /> },
  { path: "/dashboard", element: <DashboardPage /> },
  { path: "/monitoring", element: <LiveMonitoringPage /> },
  { path: "/twin", element: <DigitalTwinPage /> },
  { path: "/predictive-health", element: <PredictiveHealthPage /> },
  { path: "/simulator", element: <MissionSimulatorPage /> },
  { path: "/alerts", element: <AlertsPage /> },
  { path: "/history", element: <MissionHistoryPage /> },
  { path: "/replay/:missionId", element: <MissionReplayPage /> }
]);
