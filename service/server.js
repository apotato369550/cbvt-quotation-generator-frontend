const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;
const DATA_FILE = path.join(__dirname, 'quotations.json');

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static(__dirname));

// Initialize quotations.json if missing
function initializeData() {
  if (!fs.existsSync(DATA_FILE)) {
    fs.writeFileSync(DATA_FILE, JSON.stringify([], null, 2));
  }
}

// Read quotations
function readQuotations() {
  initializeData();
  const data = fs.readFileSync(DATA_FILE, 'utf-8');
  return JSON.parse(data);
}

// Write quotations
function writeQuotations(quotations) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(quotations, null, 2));
}

// Generate unique ID
function generateId() {
  return Date.now().toString();
}

// GET all quotations
app.get('/api/quotations', (req, res) => {
  try {
    const quotations = readQuotations();
    res.json(quotations);
  } catch (error) {
    res.status(500).json({ error: 'Failed to read quotations' });
  }
});

// POST new quotation
app.post('/api/quotations', (req, res) => {
  try {
    const quotations = readQuotations();
    const newQuotation = {
      id: generateId(),
      date_created: new Date().toISOString(),
      status: 'draft',
      ...req.body
    };
    quotations.push(newQuotation);
    writeQuotations(quotations);
    res.status(201).json(newQuotation);
  } catch (error) {
    res.status(400).json({ error: 'Failed to save quotation' });
  }
});

// GET single quotation
app.get('/api/quotations/:id', (req, res) => {
  try {
    const quotations = readQuotations();
    const quotation = quotations.find(q => q.id === req.params.id);
    if (!quotation) {
      return res.status(404).json({ error: 'Quotation not found' });
    }
    res.json(quotation);
  } catch (error) {
    res.status(500).json({ error: 'Failed to retrieve quotation' });
  }
});

// PUT update quotation
app.put('/api/quotations/:id', (req, res) => {
  try {
    const quotations = readQuotations();
    const index = quotations.findIndex(q => q.id === req.params.id);
    if (index === -1) {
      return res.status(404).json({ error: 'Quotation not found' });
    }
    quotations[index] = { ...quotations[index], ...req.body, id: req.params.id };
    writeQuotations(quotations);
    res.json(quotations[index]);
  } catch (error) {
    res.status(400).json({ error: 'Failed to update quotation' });
  }
});

// DELETE quotation
app.delete('/api/quotations/:id', (req, res) => {
  try {
    const quotations = readQuotations();
    const index = quotations.findIndex(q => q.id === req.params.id);
    if (index === -1) {
      return res.status(404).json({ error: 'Quotation not found' });
    }
    const deleted = quotations.splice(index, 1);
    writeQuotations(quotations);
    res.json(deleted[0]);
  } catch (error) {
    res.status(500).json({ error: 'Failed to delete quotation' });
  }
});

// Start server
app.listen(PORT, () => {
  initializeData();
  console.log(`Quotation generator running on http://localhost:${PORT}`);
});
