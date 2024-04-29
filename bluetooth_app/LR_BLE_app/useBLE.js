/* eslint-disable no-bitwise */
import { useState, useEffect, useMemo } from 'react'
import { PermissionsAndroid, Platform } from 'react-native'
import DeviceInfo from 'react-native-device-info';
import { atob, btoa } from 'react-native-quick-base64'
import {
    BleError,
    BleManager,
    Characteristic,
    Device,
  } from "react-native-ble-plx";

const BLE_SERVICE_UUID = 'FFE0' //dummy UUID
const BLE_SERVICE_CHARACTERISTIC = 'FFE1'//dummy characteristic    

const useBLE = () => {

    const bleManager = useMemo(() => new BleManager(), [])
    const [ connectedDevice, setConnectedDevice ] = useState(0)

    const onDeviceDisconnected = (callback) => {
        bleManager.onDeviceDisconnected((error, device) => {
            if (error) {
                console.error('An error occurred while disconnecting:', error);
            } else {
                console.log('Device disconnected:', device);
            }
            callback(device)
        });
    }

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

    const isDuplicate = (devices, newDevice) => {
        return devices.some(device => device.id === newDevice.id)
    }

    const scanAndConnect = (callback) => {
        let timeoutId = null;
        bleManager.startDeviceScan(null, { legacyScan:false }, (error, device) => {
            if (error) {
                console.log(error);
                callback(false);
            }
    
            if (
                device &&
                (device.name?.includes("DSD TECH") ||
                device.id == "68:5E:1C:5A:95:EE")
            ) {
                clearTimeout(timeoutId);
                bleManager.stopDeviceScan();
                const result = connectToDevice(device);
                callback(result);
            }
        });
    
        timeoutId = setTimeout(() => {
            bleManager.stopDeviceScan();
            callback(false);
        }, 3000); // 3 seconds
    }

    const connectToDevice = async (device) => {
        try {
            
            const connectedDevice = await bleManager.connectToDevice(device.id)
            await connectedDevice.discoverAllServicesAndCharacteristics()
            setConnectedDevice(connectedDevice)
            //startListening(connectedDevice)
            return true
        } catch(error) {
            console.error("Error in connection", error)
            return false
        }
    }


    const disconnectFromDevice = async (device) => {
        if(device) {
            await bleManager.cancelDeviceConnection(device.id)
            setConnectedDevice(null)
            alert("Disconnected From Henry")
        }
    }

    /* Update this function to receive data */
    const onUpdate = (error, characteristic) => {
        // handle the data from the characteristic
        //atob(characteristic.value)
    }

    /* Update this function to receive data */    
    const startListening = async (device) => {
        /*
        if (device) {
          device.monitorCharacteristicForService(
            BLE_SERVICE_UUID,
            BLE_SERVICE_CHARACTERISTIC,
            onUpdate,
          );
        } else {
          console.log('No Device Connected');
        }
        */
    }


    const sendCommand = async (device, command) => {

        console.log("Sending command", command)

        try {
            if(device) {
                await bleManager.writeCharacteristicWithResponseForDevice(
                    device.id,
                    BLE_SERVICE_UUID,
                    BLE_SERVICE_CHARACTERISTIC,
                    btoa(`${command}`)
                )
            } 
        } catch(error) {
            console.error("Error in sending command", error)
            alert("Disconnected From Henry")
            setConnectedDevice(null)
        }
    }

    
    return {
        requestPermissions,
        scanAndConnect,
        disconnectFromDevice,
        startListening,
        sendCommand,
        onDeviceDisconnected,
        connectedDevice,
        setConnectedDevice
    }
}


export default useBLE
