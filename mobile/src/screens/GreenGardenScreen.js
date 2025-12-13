/**
 * Green Garden Screen
 *
 * Gamification - Plant and grow virtual plants using Green Points
 */
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Dimensions,
  Alert,
} from 'react-native';
import { useApp } from '../context/AppContext';

const { width } = Dimensions.get('window');
const GRID_SIZE = 5;
const CELL_SIZE = (width - 64) / GRID_SIZE;

const GreenGardenScreen = () => {
  const { greenPoints } = useApp();
  const [garden, setGarden] = useState(generateEmptyGarden());
  const [selectedPlant, setSelectedPlant] = useState(null);

  const plants = [
    { id: 'sunflower', name: '🌻 Sunflower', cost: 100, stages: 5 },
    { id: 'olive', name: '🫒 Olive Tree', cost: 500, stages: 7 },
    { id: 'rose', name: '🌹 Rose', cost: 150, stages: 4 },
    { id: 'cactus', name: '🌵 Cactus', cost: 75, stages: 3 },
    { id: 'lemon', name: '🍋 Lemon Tree', cost: 400, stages: 6 },
    { id: 'lavender', name: '🪻 Lavender', cost: 200, stages: 4 },
  ];

  const handleCellPress = (row, col) => {
    if (!selectedPlant) {
      Alert.alert('Select Plant', 'Please select a plant from the catalog first');
      return;
    }

    if (garden[row][col]) {
      Alert.alert('Occupied', 'This spot is already occupied');
      return;
    }

    if (greenPoints < selectedPlant.cost) {
      Alert.alert(
        'Not Enough Points',
        `You need ${selectedPlant.cost} points. You have ${greenPoints}.`
      );
      return;
    }

    // Plant the selected plant
    const newGarden = [...garden];
    newGarden[row][col] = {
      ...selectedPlant,
      stage: 1,
      plantedAt: new Date(),
    };
    setGarden(newGarden);
    setSelectedPlant(null);

    Alert.alert(
      'Plant Planted! 🌱',
      `You planted a ${selectedPlant.name}. Water it regularly to help it grow!`
    );
  };

  const handleWaterPlant = (row, col) => {
    const plant = garden[row][col];
    if (!plant) return;

    if (plant.stage >= plant.stages) {
      Alert.alert('Fully Grown', 'This plant is already fully grown!');
      return;
    }

    // Water and grow
    const newGarden = [...garden];
    newGarden[row][col] = {
      ...plant,
      stage: plant.stage + 1,
    };
    setGarden(newGarden);

    if (newGarden[row][col].stage >= plant.stages) {
      Alert.alert('Congratulations! 🎉', 'Your plant has fully grown!');
    }
  };

  return (
    <ScrollView style={styles.container}>
      {/* Points Display */}
      <View style={styles.pointsCard}>
        <Text style={styles.pointsLabel}>Green Points</Text>
        <Text style={styles.pointsValue}>{greenPoints}</Text>
      </View>

      {/* Garden Grid */}
      <View style={styles.gardenCard}>
        <Text style={styles.cardTitle}>Your Green Garden</Text>
        <View style={styles.grid}>
          {garden.map((row, rowIndex) => (
            <View key={rowIndex} style={styles.row}>
              {row.map((cell, colIndex) => (
                <TouchableOpacity
                  key={`${rowIndex}-${colIndex}`}
                  style={styles.cell}
                  onPress={() =>
                    cell
                      ? handleWaterPlant(rowIndex, colIndex)
                      : handleCellPress(rowIndex, colIndex)
                  }
                >
                  {cell ? (
                    <View style={styles.plantCell}>
                      <Text style={styles.plantEmoji}>
                        {getPlantEmoji(cell.id, cell.stage, cell.stages)}
                      </Text>
                      <Text style={styles.plantStage}>
                        {cell.stage}/{cell.stages}
                      </Text>
                    </View>
                  ) : (
                    <Text style={styles.emptyCell}>+</Text>
                  )}
                </TouchableOpacity>
              ))}
            </View>
          ))}
        </View>
      </View>

      {/* Plant Catalog */}
      <View style={styles.catalogCard}>
        <Text style={styles.cardTitle}>Plant Catalog</Text>
        {plants.map((plant) => (
          <TouchableOpacity
            key={plant.id}
            style={[
              styles.plantItem,
              selectedPlant?.id === plant.id && styles.selectedPlantItem,
            ]}
            onPress={() => setSelectedPlant(plant)}
          >
            <View style={styles.plantItemLeft}>
              <Text style={styles.plantItemName}>{plant.name}</Text>
              <Text style={styles.plantItemInfo}>
                {plant.stages} growth stages
              </Text>
            </View>
            <View style={styles.plantItemRight}>
              <Text style={styles.plantItemCost}>{plant.cost}</Text>
              <Text style={styles.plantItemCostLabel}>points</Text>
            </View>
          </TouchableOpacity>
        ))}
      </View>

      {/* Instructions */}
      <View style={styles.instructionsCard}>
        <Text style={styles.instructionsTitle}>🌱 How to Play</Text>
        <Text style={styles.instructionText}>
          1. Earn Green Points by completing saving sessions
        </Text>
        <Text style={styles.instructionText}>
          2. Select a plant from the catalog
        </Text>
        <Text style={styles.instructionText}>
          3. Tap an empty spot in your garden to plant it
        </Text>
        <Text style={styles.instructionText}>
          4. Tap on planted plants to water them and help them grow!
        </Text>
      </View>
    </ScrollView>
  );
};

// Helper functions
function generateEmptyGarden() {
  return Array(GRID_SIZE)
    .fill(null)
    .map(() => Array(GRID_SIZE).fill(null));
}

function getPlantEmoji(plantId, stage, maxStages) {
  const progress = stage / maxStages;

  const emojis = {
    sunflower: ['🌱', '🌿', '🌻', '🌻', '🌻'],
    olive: ['🌱', '🌿', '🌿', '🌳', '🌳', '🫒', '🫒'],
    rose: ['🌱', '🌿', '🌹', '🌹'],
    cactus: ['🌱', '🌵', '🌵'],
    lemon: ['🌱', '🌿', '🌳', '🌳', '🍋', '🍋'],
    lavender: ['🌱', '🌿', '🪻', '🪻'],
  };

  const plantEmojis = emojis[plantId] || ['🌱'];
  const emojiIndex = Math.min(stage - 1, plantEmojis.length - 1);

  return plantEmojis[emojiIndex];
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  pointsCard: {
    backgroundColor: '#4CAF50',
    margin: 16,
    padding: 24,
    borderRadius: 16,
    alignItems: 'center',
  },
  pointsLabel: {
    color: '#FFFFFF',
    fontSize: 16,
    opacity: 0.9,
  },
  pointsValue: {
    color: '#FFFFFF',
    fontSize: 48,
    fontWeight: 'bold',
    marginTop: 8,
  },
  gardenCard: {
    backgroundColor: '#FFFFFF',
    margin: 16,
    marginTop: 0,
    padding: 20,
    borderRadius: 12,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  grid: {
    borderWidth: 2,
    borderColor: '#8BC34A',
    borderRadius: 8,
    overflow: 'hidden',
  },
  row: {
    flexDirection: 'row',
  },
  cell: {
    width: CELL_SIZE,
    height: CELL_SIZE,
    borderWidth: 1,
    borderColor: '#E0E0E0',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#FAFAFA',
  },
  emptyCell: {
    fontSize: 24,
    color: '#CCC',
  },
  plantCell: {
    alignItems: 'center',
  },
  plantEmoji: {
    fontSize: 28,
  },
  plantStage: {
    fontSize: 10,
    color: '#666',
    marginTop: 2,
  },
  catalogCard: {
    backgroundColor: '#FFFFFF',
    margin: 16,
    marginTop: 0,
    padding: 20,
    borderRadius: 12,
  },
  plantItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderRadius: 8,
    backgroundColor: '#F5F5F5',
    marginBottom: 12,
  },
  selectedPlantItem: {
    backgroundColor: '#E8F5E9',
    borderWidth: 2,
    borderColor: '#4CAF50',
  },
  plantItemLeft: {
    flex: 1,
  },
  plantItemName: {
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
  },
  plantItemInfo: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  plantItemRight: {
    alignItems: 'flex-end',
  },
  plantItemCost: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  plantItemCostLabel: {
    fontSize: 12,
    color: '#666',
  },
  instructionsCard: {
    backgroundColor: '#FFF3E0',
    margin: 16,
    marginTop: 0,
    padding: 20,
    borderRadius: 12,
  },
  instructionsTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#E65100',
    marginBottom: 12,
  },
  instructionText: {
    fontSize: 14,
    color: '#E65100',
    marginBottom: 8,
    lineHeight: 20,
  },
});

export default GreenGardenScreen;
