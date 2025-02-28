const express = require('express');
const axios = require('axios'); // ✅ Use axios to fetch from Django

const app = express();
const port = process.env.PORT || 3000;

// Django API URL (Replace with your actual Render Django URL)
const DJANGO_API_URL = 'https://crawford-car-reviews.onrender.com/djangoapp/dealerships/';

app.use(express.json());

// Define a route to get all dealerships with optional state and ID filters
app.get('/dealerships/get', async (req, res) => {
  const { state, id } = req.query;

  try {
    // ✅ Forward query parameters to Django
    const response = await axios.get(DJANGO_API_URL, { params: { state, id } });

    res.json(response.data);
  } catch (error) {
    console.error('Error fetching dealerships:', error.message);
    res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
