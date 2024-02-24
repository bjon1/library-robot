import { useState } from 'react';
import { SafeAreaView, StyleSheet, Text, ScrollView, View, Button, TouchableOpacity, Touchable, DevSettings } from 'react-native';
import DeviceModal from './components/DeviceModal';
import useBLE from './useBLE';
import robotAPI from './services/robotAPI';
import { Device } from 'react-native-ble-plx';

const App = () => {

  const DeviceCommunicator = useBLE()
    /* Device Communicator:
        requestPermissions() -> boolean
        scanForDevices() 
        connectToDevice(device) //updates connectedDevice
        disconnectFromDevice() //updates connectedDevice
        startListening(device)
        sendCommand(device, command)
        connectedDevice 
        allDevices
    */
  

  const [isModalVisible, setIsModalVisible] = useState(false);

  const pressConnect = async () => {
    try {
      const acceptedPermissions = await DeviceCommunicator.requestPermissions();
      if(acceptedPermissions) {
        DeviceCommunicator.scanForDevices();
        alert('Scanning for devices');
      }
    } catch (error) {
      // Handle any errors that occurred during permission request
      console.error("Permission request error:", error);
    }
  }
  
  const buttonData = [
    
    { title: 'Cruise', onPress: () => DeviceCommunicator.sendCommand(DeviceCommunicator.connectedDevice, 1) },
    { title: 'Go Forward', onPress: () => DeviceCommunicator.sendCommand(DeviceCommunicator.connectedDevice, 2) },
    { title: 'Go Backward', onPress: () => DeviceCommunicator.sendCommand(DeviceCommunicator.connectedDevice, 3) },
    { title: 'Turn Left', onPress: () => DeviceCommunicator.sendCommand(DeviceCommunicator.connectedDevice, 4) },
    { title: 'Turn Right', onPress: () => DeviceCommunicator.sendCommand(DeviceCommunicator.connectedDevice, 5) },
    { title: 'Stop', onPress: () => DeviceCommunicator.sendCommand(DeviceCommunicator.connectedDevice, 6)},
    { title: 'reload', onPress: () => DevSettings.reload() },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
      <View>
        {DeviceCommunicator.connectedDevice && buttonData.map((button, index) => (
          <TouchableOpacity 
            key={index}
            style={styles.button}
            onPress={button.onPress}
          >
            <Text style={styles.buttonText}>{button.title}</Text>
          </TouchableOpacity>
        ))}

        {!DeviceCommunicator.connectedDevice && DeviceCommunicator.allDevices
          .filter(device => device.rssi > -70)
          .sort((a, b) => b.rssi - a.rssi)
          .map((device, index) => (
            <TouchableOpacity
              style={styles.button}
              key={device.id}
              onPress={() => DeviceCommunicator.connectToDevice(device)}
            >
              <Text>{device.name ? device.name : "Unknown"}</Text>
              <Text>{device.id}</Text>
              <Text>{device.rssi}</Text>
            </TouchableOpacity>
        ))}

        <Text>{DeviceCommunicator.allDevices.length}</Text>
        
        <TouchableOpacity
          onPress={ DeviceCommunicator.connectedDevice ? DeviceCommunicator.disconnectFromDevice : pressConnect } 
          style={ styles.ctaButton }>
          <Text style={ styles.ctaButtonText }>
            { DeviceCommunicator.connectedDevice ? 'Disconnect' : 'Connect' }
          </Text>
        </TouchableOpacity>
      </View>
      </ScrollView>


    </SafeAreaView>
  )
}

export default App

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#abe7ff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  button: {
    backgroundColor: '#007bff',
    paddingVertical: 15,
    paddingHorizontal: 50,
    borderRadius: 8,
    marginBottom: 10,
  },
  buttonText: {
    color: 'white',
    fontSize: 20,
    textAlign: 'center',
  },
  blackText: {
    color: 'black'
  },
  ctaButton: {
    backgroundColor: 'purple',
    justifyContent: 'center',
    alignItems: 'center',
    height: 50,
    marginHorizontal: 20,
    marginBottom: 5,
    borderRadius: 8,
  },
  ctaButtonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
  },
});