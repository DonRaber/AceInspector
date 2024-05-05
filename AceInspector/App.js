import { StatusBar } from './.expo/node_modules/expo-status-bar/src/StatusBar';
import { StyleSheet, Text, View, Image } from './.expo/node_modules/react-native/types';

export default function App() {
  return (
    <View style={styles.container}>
      <Text>Ace Inspector</Text>
      <Text>Welcome</Text>
      <Image source={require('./assets/favicon.png')} />
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
