document.addEventListener("DOMContentLoaded", async function() {
    const username = "marianjosephjeffrey"; // Your GitHub username
    const apiUrl = `https://api.github.com/users/${username}/repos`;

    try {
        const response = await fetch(apiUrl);
        const projects = await response.json();

        const projectContainer = document.getElementById("projects");

        for (const project of projects) {
            const projectCard = document.createElement("div");
            projectCard.classList.add("project-card");

            // Fetch README file (raw content)
            const readmeUrl = `https://raw.githubusercontent.com/${username}/${project.name}/main/README.md`;
            let readmeContent = "No README available.";

            try {
                const readmeResponse = await fetch(readmeUrl);
                if (readmeResponse.ok) {
                    readmeContent = await readmeResponse.text();
                    readmeContent = marked.parse(readmeContent); // Convert Markdown to HTML using Marked.js
                }
            } catch (error) {
                console.warn(`Could not fetch README for ${project.name}`);
            }

            // Calculate project duration (from created_at to updated_at)
            const createdDate = new Date(project.created_at);
            const updatedDate = new Date(project.updated_at);
            const duration = Math.round((updatedDate - createdDate) / (1000 * 60 * 60 * 24)); // Days

            projectCard.innerHTML = `
                <div class="project-details">
                    <h3>${project.name.replace(/-/g, " ")}</h3>
                    <p><strong>Duration:</strong> ${duration} days</p>
                    <div class="readme-content">${readmeContent}</div> <!-- Display README here -->
                </div>
                <div class="project-links">
                    <a href="${project.html_url}" target="_blank" class="github-link">View on GitHub</a>
                </div>
            `;

            projectContainer.appendChild(projectCard);
        }
    } catch (error) {
        console.error("Error fetching GitHub projects:", error);
    }
});