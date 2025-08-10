import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useAuth } from '../context/AuthContext';

const SuperAdminHomeScreen: React.FC = () => {
    const { user, logout } = useAuth();

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Super Admin Dashboard</Text>
            <Text style={styles.welcome}>Welcome, {user?.first_name}!</Text>

            <View style={styles.menuContainer}>
                <TouchableOpacity style={styles.menuItem}>
                    <Text style={styles.menuText}>Manage Users</Text>
                </TouchableOpacity>

                <TouchableOpacity style={styles.menuItem}>
                    <Text style={styles.menuText}>System Analytics</Text>
                </TouchableOpacity>

                <TouchableOpacity style={styles.menuItem}>
                    <Text style={styles.menuText}>Business Management</Text>
                </TouchableOpacity>

                <TouchableOpacity style={styles.menuItem}>
                    <Text style={styles.menuText}>System Settings</Text>
                </TouchableOpacity>

                <TouchableOpacity style={styles.menuItem}>
                    <Text style={styles.menuText}>Audit Logs</Text>
                </TouchableOpacity>
            </View>

            <TouchableOpacity style={styles.logoutButton} onPress={logout}>
                <Text style={styles.logoutText}>Logout</Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 20,
        backgroundColor: '#fff',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        textAlign: 'center',
        marginTop: 50,
        marginBottom: 10,
    },
    welcome: {
        fontSize: 18,
        textAlign: 'center',
        marginBottom: 30,
        color: '#666',
    },
    menuContainer: {
        flex: 1,
    },
    menuItem: {
        backgroundColor: '#FF6B35',
        padding: 15,
        borderRadius: 8,
        marginBottom: 15,
    },
    menuText: {
        color: '#fff',
        fontSize: 16,
        textAlign: 'center',
        fontWeight: '500',
    },
    logoutButton: {
        backgroundColor: '#FF3B30',
        padding: 15,
        borderRadius: 8,
        marginTop: 20,
    },
    logoutText: {
        color: '#fff',
        fontSize: 16,
        textAlign: 'center',
        fontWeight: '500',
    },
});

export default SuperAdminHomeScreen;