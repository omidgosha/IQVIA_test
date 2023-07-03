import React, { useState, useEffect } from "react";
import axios from "axios";
import { Button, TextField, Select, MenuItem, FormControl, InputLabel } from "@mui/material";
import { useNavigate } from "react-router-dom";

const NewJob = () => {
 const [jobName, setJobName] = useState("");
 const [scriptName, setScriptName] = useState("");
 const [scripts, setScripts] = useState([]);
 const [currentScript, setCurrentScript] = useState(null);
 const [scriptArguments, setArguments] = useState({});

 const navigate = useNavigate();

 useEffect(() => {
  const fetchScripts = async () => {
   const response = await axios.get("/api/v1/script_names");
   setScripts(response.data);
  };
  fetchScripts();
 }, []);

 useEffect(() => {
  if (currentScript) {
   const initialArgs = {};
   currentScript["arguments"].forEach((arg) => {
    initialArgs[arg.name] = "";
   });
   setArguments(initialArgs);
  }
 }, [currentScript]);

 useEffect(() => {
  if (scriptName) {
   const _script = scripts.find((s) => s.script_name == scriptName);
   if (_script) setCurrentScript(_script);
  }
 }, [scriptName]);

 const handleArgChange = (event, argName) => {
  setArguments((prevArgs) => ({
   ...prevArgs,
   [argName]: event.target.value,
  }));
 };

 const resetForm = () => {
  setJobName("");
  setScriptName("");
  setArguments({});
 };

 const handleSubmit = async (event) => {
  event.preventDefault();
  const response = await axios.post("/api/v1/script", {
   job_name: jobName,
   script_name: scriptName,
   scriptArguments,
  });

  // If the response status is 200, redirect to the All Jobs page
  if (response.status === 201 || response.status === 200) {
   alert("Job created successfully!"); // show a pop-up message

   navigate("/all-jobs");
  } else {
   resetForm();
   alert("Job creation failed. Please try again."); // show a pop-up message
  }
 };

 return (
  <form onSubmit={handleSubmit}>
   <TextField
    variant="outlined"
    margin="normal"
    required
    fullWidth
    label="Job name"
    value={jobName}
    onChange={(e) => setJobName(e.target.value)}
   />
   <FormControl variant="outlined" margin="normal" required fullWidth>
    <InputLabel>Script</InputLabel>
    <Select value={scriptName} onChange={(e) => setScriptName(e.target.value)} label="Script">
     {scripts.map((script) => (
      <MenuItem key={script.script_name} value={script.script_name}>
       {script.script_name}
      </MenuItem>
     ))}
    </Select>
   </FormControl>
   {currentScript &&
    currentScript["arguments"].map((arg) => (
     <TextField
      variant="outlined"
      margin="normal"
      required
      fullWidth
      label={arg.name}
      type={arg.type === "string" ? "text" : "number"}
      value={scriptArguments[arg.name] || ""}
      onChange={(e) => handleArgChange(e, arg.name)}
     />
    ))}
   <Button type="submit" fullWidth variant="contained" color="primary">
    Submit
   </Button>
  </form>
 );
};

export default NewJob;
