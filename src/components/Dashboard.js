import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavigationBar from "./NavigationBar";
import NewJob from "./NewJob";
import AllJobs from "./AllJobs";

const Dashboard = () => {
 return (
  <Router>
   <div className="dashboard">
    <NavigationBar />
    <div style={{ marginLeft: "240px" }}>
     <Routes>
      <Route path="/new-job" element={<NewJob />} />
      <Route path="/all-jobs" element={<AllJobs />} />
     </Routes>
    </div>
   </div>
  </Router>
 );
};

export default Dashboard;
