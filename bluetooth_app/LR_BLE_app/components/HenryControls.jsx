import { useState } from 'react'
import { View, Text, TouchableOpacity, Image, StyleSheet } from 'react-native'
import Slider from '@react-native-community/slider';
import { responsive } from '../utils/responsive';

const orange = '#F3721B'
const blue = '#173A79'
const white = '#FAF9F9'

const HenryControls = ({ sendCommand, connectedDevice }) => {

    const [range, setRange] = useState('50');
    const [sliding, setSliding] = useState(false);
  
    const updateSlider = (value) => {
      setSliding(true);
      setRange(value);
    };

    const buttonData = [
        { title: 'Left 90', image: require('../imgs/turn-left.png'), onPress: () => sendCommand(connectedDevice, 4) },
        { title: 'Forward', image: require('../imgs/up.png'), onPress: () => sendCommand(connectedDevice, 2) },
        { title: 'Right 90', image: require('../imgs/turn-right.png'),  onPress: () => sendCommand(connectedDevice, 5) },
        
        { title: 'CCW', image: require('../imgs/CCW.png'), onPress: () => sendCommand(connectedDevice, 7) },
        { title: 'STOP', image: require('../imgs/stop.png'), onPress: () => sendCommand(connectedDevice, 8) },
        { title: 'CW', image: require('../imgs/CW.png'), onPress: () => sendCommand(connectedDevice, 6) },
    
        { title: 'Reverse', image: require('../imgs/down.png'), onPress: () => sendCommand(connectedDevice, 3) },
    
        { title: 'Cruise', image: require('../imgs/up.png'), onPress: () => sendCommand(connectedDevice, 1) },
        { title: 'STOP', image: require('../imgs/stop.png'), onPress: () => sendCommand(connectedDevice, 9) }
      ];

    return (
        <View style={styles.appContainer}>

            <View style={styles.row}>
                {buttonData.slice(0, 3).map((button, index) => (
                <TouchableOpacity key={index} style={styles.button} onPress={button.onPress}>
                    <Image source={button.image} style={styles.buttonImage} />
                </TouchableOpacity>
                ))}
            </View>

            <View style={styles.row}>
                {buttonData.slice(3, 6).map((button, index) => (
                <TouchableOpacity key={index} style={styles.button} onPress={button.onPress}>
                    <Image source={button.image} style={styles.buttonImage} />
                </TouchableOpacity>
                ))}
            </View>

            <View style={styles.row}>
                <TouchableOpacity 
                    style={[styles.button, styles.centeredButton]}
                    onPress={ () => sendCommand(connectedDevice, 3) }
                >
                <Image source={buttonData.find(button => button.title === 'Reverse').image} style={styles.buttonImage} />
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
                    onSlidingComplete={value => sendCommand(connectedDevice, parseInt(value) < 10 ? 10 : parseInt(value))}
                />
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    appContainer: {
        marginTop: responsive(60),
        justifyContent: 'center', // Center content vertically
        alignItems: 'center', // Center content horizontally
    },
    row: {
        flexDirection: 'row',
        marginBottom: responsive(0), // Adjust spacing between rows
    },
    buttonImage: {
        width: responsive(50),
        height: responsive(50),
    },
    centeredButton: {
        alignSelf: 'center',
        justifyContent: 'center',
    },
    button: {
        alignItems: 'center',
        borderRadius: responsive(100),
        borderWidth: 0.3,
        width: responsive(75),
        paddingVertical: responsive(30),
        paddingHorizontal: responsive(25),
        margin: responsive(10),
    },
    SliderView: {
        marginTop: responsive(20)
    },
    SliderText: {
        color: 'black',
        fontWeight: 'bold',
        fontSize: responsive(20),
        textAlign: 'center',
        margin: responsive(5)
    },
})

export default HenryControls