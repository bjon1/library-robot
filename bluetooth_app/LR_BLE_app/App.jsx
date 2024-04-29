import { useState, useEffect } from 'react';
import { SafeAreaView, StyleSheet, Text, Image, ScrollView, View, Button, TouchableOpacity, Touchable, DevSettings } from 'react-native'
import Orientation from 'react-native-orientation-locker';
import { responsive } from './utils/responsive';

import useBLE from './useBLE';
import HenryConnected from './components/HenryConnected';

const orange = '#F3721B'
const blue = '#173A79'
const white = '#FAF9F9'
const App = () => {

  useEffect(() => {
    onDeviceDisconnected((device) => {
      alert("Disconnected from Henry")
      setConnectedDevice(null);
    })
    Orientation.lockToPortrait();

    return () => {
      Orientation.unlockAllOrientations();
    };
  }, [])


  const { requestPermissions, scanAndConnect, disconnectFromDevice, onDeviceDisconnected, sendCommand, connectedDevice, setConnectedDevice } = useBLE()


  const pressConnect = async () => {
    try {
      const acceptedPermissions = await requestPermissions();
      if(acceptedPermissions) {
        scanAndConnect((callback) => {
          if(callback) {
            alert("Successfully Connected to Henry")
          } else {
            alert("Failed to connect to Henry. Try again later")
          }
        });
      }
    } catch (error) {
      // Handle any errors that occurred during permission request
      console.error("Permission request error:", error);
    }
  }

  const pressDisconnect = async () => {
    await sendCommand(connectedDevice, 8); // stop the robot
    await disconnectFromDevice(connectedDevice);
  }
  

  return (
    <SafeAreaView style={styles.appScreen}>

      {connectedDevice ? (
        <HenryConnected                     
          sendCommand={sendCommand} 
          disconnectFromDevice={disconnectFromDevice} 
          connectedDevice={connectedDevice}
        />
      ) : (
        <TouchableOpacity
          onPress={ connectedDevice ? pressDisconnect : pressConnect } 
          style={ styles.Button }
        >
          <Text style={ styles.ButtonText }>
            { connectedDevice ? 'Disconnect' : 'Connect' }
          </Text>
        </TouchableOpacity>
      )}
    
    </SafeAreaView>
  )
}


const styles = StyleSheet.create({
  appScreen: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: white,
  },
  appContainer: {
    justifyContent: 'center', // Center content vertically
    alignItems: 'center', // Center content horizontally
  },
  Button: {
    backgroundColor: blue,
    justifyContent: 'center',
    alignItems: 'flex-end',
    paddingVertical: responsive(30),
    paddingHorizontal: responsive(50),
    borderRadius: responsive(100),
  },
  ButtonText: {
    fontSize: responsive(25),
    fontWeight: 'bold',
    color: white,
  },
});

export default App