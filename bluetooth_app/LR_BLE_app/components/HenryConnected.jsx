import { useState } from 'react';
import { View, Text, Image, StyleSheet, TouchableOpacity } from 'react-native'
import { responsive } from '../utils/responsive';

import Menu from './Menu'
import HenryControls from './HenryControls'


const HenryConnected = ({sendCommand, disconnectFromDevice, connectedDevice}) => {

    const [isMenuOpen, setIsMenuOpen] = useState(false);
    
    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen)
    }

    return (
        <View style={styles.henryConnected}>
            <View style={styles.henryConnectedContainer}>
                <TouchableOpacity style={styles.buttonMenu} onPress={ () => toggleMenu()}>
                    <Image source={require('../imgs/menu.png')} style={styles.buttonImage} />
                </TouchableOpacity>
                <Text style={styles.buttonText}>Menu</Text>
            </View>


            {isMenuOpen ? (
                <Menu
                    sendCommand={sendCommand} 
                    disconnectFromDevice={disconnectFromDevice} 
                    connectedDevice={connectedDevice}
                />
            ) : (
                <HenryControls 
                    sendCommand={sendCommand} 
                    connectedDevice={connectedDevice}
                />
            )}
        </View>
    )
}

const styles = StyleSheet.create({
    henryConnected: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    henryConnectedContainer: {
        flexDirection: 'row',
        gap: responsive(15),
        alignItems: 'center',
        width: '100%',
        paddingHorizontal: responsive(20),
        marginBottom: responsive(25),
    },
    buttonText: {
        fontSize: responsive(25),
        fontWeight: 'bold',
        color: 'black',
    },    
    buttonImage: {
        width: responsive(50),
        height: responsive(50),
    },
})

export default HenryConnected