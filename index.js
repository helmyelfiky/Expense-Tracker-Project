const { app, BrowserWindow } = require('electron');
const { exec } = require('child_process');
const path = require('path');

let mainWindow;

// Function to create the main browser window
function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js') // You may keep this if needed
        }
    });

    // Load the Django app
    mainWindow.loadURL('http://127.0.0.1:8000');
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

// Start Django server and open the window
app.on('ready', () => {
    const server = exec('python manage.py runserver', {
        cwd: path.join(__dirname, 'Expense-Tracker') // Corrected path to the folder where manage.py is located
    });

    // Wait for Django to be ready before opening the Electron window
    server.stdout.on('data', data => {
        console.log(data.toString());
        if (data.includes('Starting development server at http://127.0.0.1:8000/')) {
            createWindow(); // Open Electron window after server is ready
        }
    });

    server.stderr.on('data', data => console.error(data.toString()));
});

// Quit when all windows are closed
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});
