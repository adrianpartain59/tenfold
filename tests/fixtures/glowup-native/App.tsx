import { useEffect } from "react";
import { ActivityIndicator, StyleSheet, Text, TextInput, View } from "react-native";
import * as Notifications from "expo-notifications";

export default function App({ loading }: { loading: boolean }) {
  useEffect(() => {
    Notifications.requestPermissionsAsync();
  }, []);
  if (loading) {
    return <ActivityIndicator size="large" />;
  }
  return (
    <View style={styles.screen}>
      <Text style={styles.title}>Welcome to your dashboard</Text>
      <TextInput style={styles.input} placeholder="Email address" />
      <View style={styles.card}><Text style={styles.body}>Oops! Something went wrong</Text></View>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, padding: 20, backgroundColor: "#F9FAFB" },
  title: { fontSize: 28, fontWeight: "700", color: "#111827", marginBottom: 12 },
  input: { fontSize: 14, borderWidth: 1, borderColor: "#E5E7EB", borderRadius: 8, padding: 10 },
  card: { marginTop: 16, padding: 16, borderRadius: 12, backgroundColor: "#fff", shadowColor: "#000", shadowOpacity: 0.1, shadowRadius: 6, elevation: 3 },
  body: { fontSize: 16, color: "#6B7280" },
});
