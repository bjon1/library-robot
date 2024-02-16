import { StatusBar } from 'expo-status-bar';
import { useState } from 'react';
import { SafeAreaView, StyleSheet, Text, View, Button, TouchableOpacity } from 'react-native';
import StopModal from './components/StopModal'

export default function App() {

  const [isModalVisible, setIsModalVisible] = useState(false);

  const hideModal = () => {
    setIsModalVisible(false); 
  }

  const showModal = () => {
    setIsModalVisible(true);
  }

  const buttonData = [
    { title: 'Cruise', onPress: () => console.log('Cruise') },
    { title: 'Go Forward', onPress: () => console.log('Go Forward') },
    { title: 'Go Backward', onPress: () => console.log('Go Backward') },
    { title: 'Turn Left', onPress: () => console.log('Turn Left') },
    { title: 'Turn Right', onPress: () => console.log('Turn Right') },
    { title: 'Stop', onPress: showModal },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <View>
        {!isModalVisible && buttonData.map((button, index) => (
          <TouchableOpacity 
            key={index}
            onPress={button.onPress}
            style={styles.button}
          >
            <Text style={styles.buttonText}>{button.title}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#abe7ff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  button: {
    backgroundColor: '#007bff',
    paddingVertical: 30,
    paddingHorizontal: 20,
    borderRadius: 8,
    marginBottom: 10,
  },
  buttonText: {
    color: 'white',
    fontSize: 20,
    textAlign: 'center',
  },
});