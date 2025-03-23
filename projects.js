document.addEventListener("DOMContentLoaded", async function () {
  const username = "marianjosephjeffrey";
  const apiUrl = `https://api.github.com/users/${username}/repos`;

  try {
    const response = await fetch(apiUrl);
    const projects = await response.json();

    const projectContainer = document.getElementById("projects");

    for (const project of projects) {
      const projectCard = document.createElement("div");
      projectCard.classList.add("project-card");

      // Try to fetch details.md instead of README.md
      const detailsUrl = `https://raw.githubusercontent.com/${username}/${project.name}/main/details.md`;
      let detailsContent = "<em>No details available.</em>";

      try {
        const detailsResponse = await fetch(detailsUrl);
        if (detailsResponse.ok) {
          const rawMarkdown = await detailsResponse.text();
          detailsContent = marked.parse(rawMarkdown); // Convert Markdown to HTML using Marked.js
        }
      } catch (err) {
        console.warn(`No details.md found in ${project.name}`);
      }

      projectCard.innerHTML = `
        <div class="project-details">
          <h3>${project.name.replace(/-/g, " ")}</h3>
          <div class="details-content">${detailsContent}</div>
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