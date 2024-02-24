/* eslint-disable no-bitwise */
import { useState, useMemo } from 'react'
import { PermissionsAndroid, Platform } from 'react-native'
import DeviceInfo from 'react-native-device-info';
import { atoa, btoa } from 'react-native-quick-base64'
import {
    BleError,
    BleManager,
    Characteristic,
    Device,
  } from "react-native-ble-plx";

const BLE_NAME = 'DUMMY_NAME'
const BLE_SERVICE_UUID = 'FFE0' //dummy UUID
const BLE_SERVICE_CHARACTERISTIC = 'FFE1'//dummy characteristic    

//BluetoothAPI:
//requestPermissions(): Promise<boolean>
//scanForPeripherals(): void

const useBLE = () => {

    const bleManager = useMemo(() => new BleManager(), [])
    const [ connectedDevice, setConnectedDevice ] = useState(null)
    const [ allDevices, setAllDevices ] = useState([])
    
    const requestAndroid31Permissions = async () => {
        const bluetoothScanPermission = await PermissionsAndroid.request(
            PermissionsAndroid.PERMISSIONS.BLUETOOTH_SCAN,
                {
                title: "Location Permission",
                message: "Bluetooth Low Energy requires Location",
                buttonPositive: "OK",
                }
        );
        const bluetoothConnectPermission = await PermissionsAndroid.request(
            PermissionsAndroid.PERMISSIONS.BLUETOOTH_CONNECT,
                {
                    title: "Location Permission",
                    message: "Bluetooth Low Energy requires Location",
                    buttonPositive: "OK",
                }
        );
        const fineLocationPermission = await PermissionsAndroid.request(
            PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
                {
                    title: "Location Permission",
                    message: "Bluetooth Low Energy requires Location",
                    buttonPositive: "OK",
                }
        );
    
        return (
          bluetoothScanPermission === "granted" &&
          bluetoothConnectPermission === "granted" &&
          fineLocationPermission === "granted"
        )
    }

    
    const requestPermissions = async () => {
        if (Platform.OS === "android") {
            const apiLevel = await DeviceInfo.getApiLevel();
            if (((apiLevel ?? -1) < 31)) {
                const granted = await PermissionsAndroid.request(
                    PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
                        {
                        title: "Location Permission",
                        message: "Bluetooth Low Energy requires Location",
                        buttonPositive: "OK",
                        }
                );
                return granted === PermissionsAndroid.RESULTS.GRANTED;
            } else {
                const isAndroid31PermissionsGranted =
                    await requestAndroid31Permissions();

                return isAndroid31PermissionsGranted;
            }
        } else {
            return true;
        }
    }
    
    // isDuplicate() checks if the new device is already in the list of devices
    const isDuplicate = (devices, newDevice) => {
        return devices.some(device => device.id === newDevice.id)
    }

    const scanForDevices = () => {
        bleManager.startDeviceScan( null , { legacyScan:false } , (error, device) => {
            if(error) {
                console.log(error)
            }

            if(device && !isDuplicate(allDevices, device)) { // if we found a unique device, add it to the list of devices
                setAllDevices(prevState => { 
                    if(!isDuplicate(prevState, device)) {
                        return [...prevState, device]
                    } else {
                        return prevState
                    }
                })
            }
        })
    }

    const connectToDevice = async (device) => {
        try {
            const connectedDevice = await bleManager.connectToDevice(device.id)
            setConnectedDevice(connectedDevice)
            await connectedDevice.discoverAllServicesAndCharacteristics()
            bleManager.stopDeviceScan()
            startListening(connectedDevice)
        } catch(error) {
            console.error("Error in connection", error)
        }
    }

    const disconnectFromDevice = async () => {
        if(connectedDevice) {
            bleManager.cancelDeviceConnection(connectedDevice.id)
            setConnectedDevice(null)
        }
    }

    /*

    const onUpdate = (error, characteristic) => {
        // handle the data from the characteristic
        //atob(characteristic.value)
        pass
*/

    const startListening = async (device) => {
        if (device) {
          device.monitorCharacteristicForService(
            BLE_SERVICE_UUID,
            BLE_SERVICE_CHARACTERISTIC,
            onUpdate,
          );
        } else {
          console.log('No Device Connected');
        }
    }


    const sendCommand = async (device, command) => {
        try {
            if(connectedDevice) {
                await bleManager.writeCharacteristicWithResponseForDevice(
                    device.id,
                    BLE_SERVICE_UUID,
                    BLE_SERVICE_CHARACTERISTIC,
                    btoa(`${command}`)
                )
            }
        } catch(error) {
            console.error("Error in sending command", error)
        }
    }

    
    return {
        requestPermissions,
        scanForDevices,
        connectToDevice,
        disconnectFromDevice,
        startListening,
        sendCommand,
        connectedDevice,
        allDevices
    }
}


export default useBLE
