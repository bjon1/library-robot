import { View, Text, StyleSheet, TouchableOpacity } from "react-native"
import { responsive } from '../utils/responsive';

const orange = '#F3721B'
const blue = '#173A79'
const white = '#FAF9F9'

const Menu = ({ sendCommand, disconnectFromDevice, connectedDevice }) => {

    const pressDisconnect = async () => {
        await sendCommand(connectedDevice, 8); // stop the robot
        await disconnectFromDevice(connectedDevice);
    }

    return(
        <View>
            <TouchableOpacity
                style={ styles.Button }
                onPress={ connectedDevice ? pressDisconnect : console.log("No device connected")} 
            >
                <Text style={ styles.ButtonText }>
                    { connectedDevice ? 'Disconnect' : 'Connect' }
                </Text>
            </TouchableOpacity>
        </View>
    )
}

const styles = StyleSheet.create({
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
})

export default Menu