import { useState, useEffect } from 'react';
import { SafeAreaView, StyleSheet, Text, ScrollView, View, Button, TouchableOpacity, Touchable, DevSettings } from 'react-native'
import Orientation from 'react-native-orientation-locker';

import DeviceModal from './components/DeviceModal';
import useBLE from './useBLE';
import robotAPI from './services/robotAPI';
import { Device } from 'react-native-ble-plx';
import { responsive } from './utils/responsive';
import Slider from '@react-native-community/slider';

const orange = '#F3721B'
const blue = '#173A79'
const white = '#FAF9F9'


const App = () => {

  useEffect(() => {
    Orientation.lockToPortrait();

    return () => {
      Orientation.unlockAllOrientations();
    };
  }, [])

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

  const [range, setRange] = useState('50');
  const [sliding, setSliding] = useState(false);

  const updateSlider = (value) => {
    setSliding(true);
    setRange(value);
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

  const pressDisconnect = async () => {
    setRange('50') //reset the speed slider value
    await sendCommand(connectedDevice, 8); // stop the robot
    await disconnectFromDevice();
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
      {connectedDevice && (
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

          <View style={styles.SliderView}>
              <Text style = { styles.SliderText }>{parseInt(range) + '%'}</Text>
              <Slider
                style={{width: 300, height: 40}}
                minimumValue={0}
                maximumValue={100}
                minimumTrackTintColor={orange}
                maximumTrackTintColor='#000'
                value={50}
                onValueChange={value => updateSlider(value)}
                onSlidingComplete={value => sendCommand(connectedDevice, parseInt(value))}
              />
          </View>
        </View>
      )}

      <TouchableOpacity
        onPress={ connectedDevice ? pressDisconnect : pressConnect } 
        style={ styles.Button }
      >
        <Text style={ styles.ButtonText }>
          { connectedDevice ? 'Disconnect' : 'Connect' }
        </Text>
      </TouchableOpacity>

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
  SliderView: {
    margin: responsive(30)
  },
  SliderText: {
    color: 'black',
    fontWeight: 'bold',
    fontSize: responsive(20),
    textAlign: 'center',
    margin: responsive(10)
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
    color: 'white',
  },
});

export default App