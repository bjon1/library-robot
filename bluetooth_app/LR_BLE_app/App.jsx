import { useState, useEffect } from 'react';
import { SafeAreaView, StyleSheet, Text, ScrollView, View, Button, TouchableOpacity, Touchable, DevSettings } from 'react-native'

import DeviceModal from './components/DeviceModal';
import useBLE from './useBLE';
import robotAPI from './services/robotAPI';
import { Device } from 'react-native-ble-plx';
import { responsive } from './utils/responsive';

const App = () => {

  const { requestPermissions, scanAndConnect, connectToDevice, disconnectFromDevice, sendCommand, connectedDevice, allDevices } = useBLE()
    /* Device Communicator:
        requestPermissions() -> boolean
        scanAndConnect() 
        connectToDevice(device) //updates connectedDevice
        disconnectFromDevice() //updates connectedDevice
        startListening(device)
        sendCommand(device, command)
        connectedDevice 
        allDevices
    */

  const [sliderValue, setSliderValue] = useState(0);

  const onSliderValueChange = (value) => {
    setSliderValue(value);
  };

  const pressConnect = async () => {
    try {
      const acceptedPermissions = await requestPermissions();
      if(acceptedPermissions) {
        scanAndConnect();
      }
    } catch (error) {
      // Handle any errors that occurred during permission request
      console.error("Permission request error:", error);
    }
  }
  
  const buttonData = [
    { title: 'Left 90', onPress: () => sendCommand(connectedDevice, 4) },
    { title: 'Forward', onPress: () => sendCommand(connectedDevice, 2) },
    { title: 'Right 90', onPress: () => sendCommand(connectedDevice, 5) },
    
    { title: 'CCW', onPress: () => sendCommand(connectedDevice, 7) },
    { title: 'STOP', onPress: () => sendCommand(connectedDevice, 8) },
    { title: 'CW', onPress: () => sendCommand(connectedDevice, 6) },

    { title: 'Reverse', onPress: () => sendCommand(connectedDevice, 3) },

    { title: 'Cruise', onPress: () => sendCommand(connectedDevice, 1) },
    { title: 'STOP', onPress: () => sendCommand(connectedDevice, 9) }
  ];

  return (
    <SafeAreaView style={styles.appScreen}>
      <View style={ styles.appContainer}>
        <View style={styles.row}>
          {buttonData.slice(0, 3).map((button, index) => (
            <TouchableOpacity key={index} style={styles.button} onPress={button.onPress}>
              <Text style={styles.buttonText}>{button.title}</Text>
            </TouchableOpacity>
          ))}
        </View>
 
        <View style={styles.row}>
          {buttonData.slice(3, 6).map((button, index) => (
            <TouchableOpacity key={index} style={styles.button} onPress={button.onPress}>
              <Text style={styles.buttonText}>{button.title}</Text>
            </TouchableOpacity>
          ))}
        </View>

        <View style={styles.row}>
          <TouchableOpacity 
            style={[styles.button, styles.centeredButton]}
            onPress={ () => sendCommand(connectedDevice, 3) }
          >
            <Text style={styles.buttonText}>Reverse</Text>
          </TouchableOpacity>
        </View>





        <TouchableOpacity
          onPress={ connectedDevice ? disconnectFromDevice : pressConnect } 
          style={ styles.Button }
        >
          <Text style={ styles.ButtonText }>
            { connectedDevice ? 'Disconnect' : 'Connect' }
          </Text>
        </TouchableOpacity>

      </View>
    </SafeAreaView>
  )
}

const orange = '#F3721B'
const blue = '#173A79'
const white = '#FAF9F9'

const styles = StyleSheet.create({
  appScreen: {
    flex: 1,
    backgroundColor: '#FAF9F9',
  },
  appContainer: {
    flex: 1,
    justifyContent: 'center', // Center content vertically
    alignItems: 'center', // Center content horizontally
  },
  row: {
    flexDirection: 'row',
    marginBottom: responsive(10), // Adjust spacing between rows
  },
  button: {
    alignItems: 'center',
    borderWidth: 1,
    width: responsive(95),
    paddingVertical: responsive(40),
    paddingHorizontal: responsive(25),
    margin: responsive(10),
  },
  buttonText: {
    color: 'black',
  },
  centeredButton: {
    alignSelf: 'center',
    justifyContent: 'center',
  },
  Button: {
    backgroundColor: 'purple',
    justifyContent: 'center',
    alignItems: 'flex-end',
    paddingVertical: responsive(30),
    paddingHorizontal: responsive(50),
    borderRadius: responsive(100),
  },
  ButtonText: {
    fontSize: responsive(25),
    fontWeight: 'bold',
    color: 'white',
  },
});

export default App