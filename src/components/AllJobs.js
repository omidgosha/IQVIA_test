import React, { useState, useEffect } from "react";
import axios from "axios";
import {
 Box,
 Paper,
 Table,
 TableBody,
 TableCell,
 TableContainer,
 TableHead,
 TableRow,
} from "@mui/material";

const AllJobs = () => {
 const [jobs, setJobs] = useState([]);

 useEffect(() => {
  const fetchJobs = async () => {
   const response = await axios.get("/api/v1/script");
   setJobs(response.data);
   console.log(response.data);
  };

  // Call fetchJobs immediately and every 5 seconds afterwards
  fetchJobs();
  const intervalId = setInterval(fetchJobs, 5000);

  // Clear the interval when the component is unmounted
  return () => clearInterval(intervalId);
 }, []);

 return (
  <Box sx={{ width: "100%", overflowX: "auto" }}>
   <TableContainer component={Paper}>
    <Table sx={{ minWidth: 650 }} aria-label="simple table">
     <TableHead>
      <TableRow>
       <TableCell>Job Name</TableCell>
       <TableCell>Job Author</TableCell>
       <TableCell>Creation Time</TableCell>
       <TableCell>Description</TableCell>
       <TableCell>Status</TableCell>
      </TableRow>
     </TableHead>
     <TableBody>
      {jobs &&
       jobs.map((job) => (
        <TableRow key={job.id}>
         <TableCell>{job.job_name}</TableCell>
         <TableCell>{job.author}</TableCell>
         <TableCell>{new Date(job.creationTime).toLocaleString()}</TableCell>
         <TableCell>{job.description}</TableCell>
         <TableCell>{job.status}</TableCell>
        </TableRow>
       ))}
     </TableBody>
    </Table>
   </TableContainer>
  </Box>
 );
};

export default AllJobs;
