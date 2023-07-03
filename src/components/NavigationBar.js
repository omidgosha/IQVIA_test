import { List, ListItem, ListItemText, Drawer } from "@mui/material";
import { makeStyles } from "@mui/styles";
import React from "react";
import { Link as RouterLink } from "react-router-dom";

const useStyles = makeStyles({
 drawer: {
  width: 240, // width of the Drawer
  flexShrink: 0,
 },
 drawerPaper: {
  width: 240, // width of the Drawer
 },
});

const NavigationBar = () => {
 const classes = useStyles();

 return (
  <Drawer
   className={classes.drawer}
   variant="permanent"
   anchor="left"
   classes={{
    paper: classes.drawerPaper,
   }}>
   <List>
    {["All Jobs", "New Job"].map((text, index) => (
     <ListItem
      button
      key={text}
      component={RouterLink}
      to={`/${text.toLowerCase().replace(/\s/g, "-")}`}>
      <ListItemText primary={text} />
     </ListItem>
    ))}
   </List>
  </Drawer>
 );
};

export default NavigationBar;
