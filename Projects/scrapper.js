const express = require("express");
const axios = require("axios");
const cheerio = require("cheerio");
const cors = require("cors");

const app = express();
app.use(cors()); // Enable CORS for frontend access

const linkedInURL = "https://www.linkedin.com/in/marianjohn";

app.get("/fetch-projects", async (req, res) => {
    try {
        const { data } = await axios.get(linkedInURL);
        const $ = cheerio.load(data);

        let projects = [];
        $(".projects__item").each((index, element) => {
            const title = $(element).find(".projects__title").text().trim();
            const description = $(element).find(".projects__description").text().trim();
            projects.push({ title, description });
        });

        res.json({ projects });
    } catch (error) {
        console.error("Error scraping LinkedIn:", error);
        res.status(500).json({ error: "Failed to fetch LinkedIn projects" });
    }
});

app.listen(3000, () => console.log("Server running on port 3000"));