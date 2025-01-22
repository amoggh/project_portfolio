const express = require('express');
const path = require('path');
const multer = require('multer');
const fs = require('fs').promises;
const fsSync = require('fs');
const app = express();


// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/')
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + '-' + file.originalname)
    }
});

const upload = multer({ storage: storage });

// Serve static files from public directory
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes for your HTML pages
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'home.html'));
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.get('/signup', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'signup.html'));
});

app.get('/index', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index1.html'));
});

// Handle portfolio submission
app.post('/submit', upload.fields([
    { name: 'photo', maxCount: 1 },
    { name: 'resume', maxCount: 1 }
]), async (req, res) => {
    try {
        const { name, education, bio, job, projects, skills } = req.body;

        // Create a unique identifier for the portfolio
        const portfolioId = `${name.toLowerCase().replace(/\s+/g, '-')}-${Date.now()}`;
        
        // Create portfolio directory
        const portfolioDir = path.join(__dirname, 'public', 'portfolios', portfolioId);
        await fs.mkdir(portfolioDir, { recursive: true });

        // Handle file uploads
        if (req.files) {
            if (req.files.photo) {
                const photoPath = path.join(portfolioDir, 'photo' + path.extname(req.files.photo[0].originalname));
                await fs.rename(req.files.photo[0].path, photoPath);
            }
            
            if (req.files.resume) {
                const resumePath = path.join(portfolioDir, 'resume' + path.extname(req.files.resume[0].originalname));
                await fs.rename(req.files.resume[0].path, resumePath);
            }
        }

        // Generate portfolio URL
        const portfolioUrl = `/portfolios/${portfolioId}`;

        res.json({
            success: true,
            message: 'Portfolio created successfully!',
            portfolioUrl: portfolioUrl
        });

    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({
            success: false,
            message: 'Error creating portfolio. Please try again.'
        });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something went wrong!');
});

// Create required directories if they don't exist
async function createRequiredDirectories() {
    const directories = ['public', 'uploads', 'public/portfolios'];
    for (const dir of directories) {
        try {
            if (!fsSync.existsSync(dir)) {
                await fs.mkdir(dir, { recursive: true });
            }
        } catch (error) {
            console.error(`Error creating directory ${dir}:`, error);
        }
    }
}

// Initialize directories and start the server
const port = 3001;

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
