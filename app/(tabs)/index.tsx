import React from 'react';
import { View, Text, Image, TouchableOpacity, StatusBar, StyleSheet } from 'react-native';
import { registerRootComponent } from 'expo';


// Farmers image URL (Replace this with a real image)
const farmersImage = "https://source.unsplash.com/800x600/?farmers,agriculture";

const App: React.FC = () => {
  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" />

      {/* Header Image */}
      <Image source={{ uri: farmersImage }} style={styles.headerImage} />

      {/* App Title */}
      <Text style={styles.title}>Caritas Farmers</Text>
      <Text style={styles.subtitle}>Empowering Farmers, Nourishing Communities</Text>

      {/* Buttons */}
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.primaryButton}>
          <Text style={styles.buttonText}>Get Started</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.secondaryButton}>
          <Text style={styles.buttonText}>Login</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

// Styles for UI
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#2E7D32', // Dark green for farming theme
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  headerImage: {
    width: '100%',
    height: 250,
    borderRadius: 20,
    marginBottom: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    color: '#f8f8f8',
    textAlign: 'center',
    marginBottom: 30,
  },
  buttonContainer: {
    width: '100%',
    alignItems: 'center',
  },
  primaryButton: {
    width: '80%',
    backgroundColor: '#FFD700', // Gold color
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 10,
    elevation: 5,
  },
  secondaryButton: {
    width: '80%',
    backgroundColor: '#FF8C00', // Orange color
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    elevation: 5,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

// Register root component (Expo or React Native)
registerRootComponent(App);

export default App;
