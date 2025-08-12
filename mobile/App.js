import React, { useState } from 'react';
import { SafeAreaView, View, Text, TextInput, Button, ScrollView } from 'react-native';

const API_BASE_URL = 'http://localhost:8000'; // change if running on device

export default function App() {
  const [mileage, setMileage] = useState('60000');
  const [lastService, setLastService] = useState('16000');
  const [battery, setBattery] = useState('11.7');
  const [coolant, setCoolant] = useState('108');
  const [tires, setTires] = useState('28,30,31,29');
  const [result, setResult] = useState(null);

  const predict = async () => {
    const tire_pressures_psi = tires
      .split(',')
      .map((t) => parseFloat(t.trim()))
      .filter((n) => !isNaN(n));

    const payload = {
      vehicle_type: 'car',
      mileage_km: parseFloat(mileage),
      last_service_km_ago: parseFloat(lastService),
      battery_voltage_v: parseFloat(battery),
      coolant_temp_c: parseFloat(coolant),
      tire_pressures_psi,
      symptoms: ['engine_rattling'],
    };

    try {
      const res = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      setResult({ error: e.message });
    }
  };

  return (
    <SafeAreaView style={{ flex: 1 }}>
      <ScrollView contentContainerStyle={{ padding: 16 }}>
        <Text style={{ fontSize: 20, fontWeight: 'bold' }}>VehicleGuard (MVP)</Text>

        <View style={{ marginTop: 12 }}>
          <Text>Mileage (km)</Text>
          <TextInput value={mileage} onChangeText={setMileage} keyboardType="numeric" style={{ borderWidth: 1, padding: 8 }} />
        </View>

        <View style={{ marginTop: 12 }}>
          <Text>Last service (km ago)</Text>
          <TextInput value={lastService} onChangeText={setLastService} keyboardType="numeric" style={{ borderWidth: 1, padding: 8 }} />
        </View>

        <View style={{ marginTop: 12 }}>
          <Text>Battery voltage (V)</Text>
          <TextInput value={battery} onChangeText={setBattery} keyboardType="numeric" style={{ borderWidth: 1, padding: 8 }} />
        </View>

        <View style={{ marginTop: 12 }}>
          <Text>Coolant temp (°C)</Text>
          <TextInput value={coolant} onChangeText={setCoolant} keyboardType="numeric" style={{ borderWidth: 1, padding: 8 }} />
        </View>

        <View style={{ marginTop: 12 }}>
          <Text>Tire pressures (psi, comma-separated)</Text>
          <TextInput value={tires} onChangeText={setTires} keyboardType="default" style={{ borderWidth: 1, padding: 8 }} />
        </View>

        <View style={{ marginTop: 16 }}>
          <Button title="Predict" onPress={predict} />
        </View>

        {result && (
          <View style={{ marginTop: 16 }}>
            <Text style={{ fontWeight: 'bold' }}>Health score: {result.health_score ?? '—'}</Text>
            <Text>Issues:</Text>
            {(result.issues || []).map((i, idx) => (
              <Text key={idx}>- {i.issue_type} ({i.severity}) {Math.round(i.probability * 100)}%: {i.recommendation}</Text>
            ))}
            {result.notes && <Text>Notes: {result.notes}</Text>}
            {result.error && <Text style={{ color: 'red' }}>Error: {result.error}</Text>}
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}