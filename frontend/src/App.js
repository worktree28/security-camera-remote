import './App.css';
import { useEffect, useState } from 'react';
import { initializeApp } from "firebase/app";
import { getMessaging, onMessage, getToken } from "firebase/messaging";
import Nav from "./Nav";
import { Grid, Box, Container, Typography, List, ListItemAvatar, Avatar, ListItemText, ListItem, Button } from '@mui/material';
function App() {
  // Your web app's Firebase configuration
  const firebaseConfig = {
    apiKey: "AIzaSyBko2mdKyIdD3XA-bh4_c-x7fE_6jRMfJs",
    authDomain: "django-notific.firebaseapp.com",
    projectId: "django-notific",
    storageBucket: "django-notific.appspot.com",
    messagingSenderId: "973143074266",
    appId: "1:973143074266:web:d1690cce1bba95a84ccce3"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const messaging = getMessaging(app);
  onMessage(messaging, (payload) => {
    console.log('Message received. ', payload);
    setUpdate(!update)
    // ...
  });
  getToken(messaging, { vapidKey: 'BBQ-2f542RYFF52OMYBb4IXsarQ2bGy1Yx3Upyhti6AuFZ5_Hw-LjfnVm2EKS1yTOEWyzlm2kkpHHu1IwG8XE1c' }).then((currentToken) => {
    if (currentToken) {
      console.log(currentToken)
      // Send the token to your server and update the UI if necessary
      // ...
    } else {
      // Show permission request UI
      console.log('No registration token available. Request permission to generate one.');
      // ...
    }
  }).catch((err) => {
    console.log('An error occurred while retrieving token. ', err);
    // ...
  });
  useEffect(() => {
    if (Notification.permission === 'granted') {
      //(new Notification('Hi there!'));
    }
    else {
      Notification.requestPermission().then(permission => (
        permission === 'granted' ? (new Notification('first!')) : null
      ));
    }
  }, []);
  const axios = require("axios");
  const [loading, setLoading] = useState(true);
  const [recent, setRecent] = useState([]);
  const [update, setUpdate] = useState(false);
  useEffect(() => {
    axios({ method: 'GET', url: 'http://127.0.0.1:8000/api/recent' })
      .then(res => res.data)
      .then(data => {
        console.log(data);
        //console.log(Object.entries(data).map(([key, item])=> <img src={item.img_url} alt="face"/>))
        setLoading(false);
        setRecent(Object.entries(data).map(([key, item], i) =>
        (
          <a href={item.img_url} target="blank" key={i}>
            <ListItem>
              <ListItemAvatar >
                <Avatar alt="face" src={item.img_url} />
              </ListItemAvatar>
              <ListItemText primary="time" secondary={item.time} />
            </ListItem>
          </a>
        )
        ))
        console.log(recent)
      })
      .catch(err => console.log(err));
    return () => { setRecent([]); setLoading(true); }
  }, [update]);

  // const something = <>

  // </>;
  return (
    <Box>
      <Nav />
      <Container maxWidth="xl">
        <Grid container spacing={3} mt={'5vh'} padding="20px">
          <Grid item xs={12} sm={6}>
            <h2> Live Cam</h2>
            <img src="http://127.0.0.1:8000/stream/test" alt="livestream" />
          </Grid>
          <Grid item xs={12} sm={6} >
            <List>
              {loading ? <Typography variant="h6" gutterBottom>Loading...</Typography> : <>
                <Grid container>
                  <Grid item>
                    <h2>History</h2>
                  </Grid>
                  <Grid item style={{ marginLeft: 'auto', marginTop: '10px' }}>
                    <Button variant="contained">Show all</Button>
                  </Grid>
                </Grid>
                {recent}
              </>}
            </List>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default App;
