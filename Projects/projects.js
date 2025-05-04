document.addEventListener("DOMContentLoaded", async function () {
  console.log("✅ DOMContentLoaded triggered");
  const username = "marianjosephjeffrey";
  const apiUrl = `https://api.github.com/users/${username}/repos`;
  console.log("🌐 Fetching repos from:", apiUrl);

  // Repos to exclude
  const excludedRepos = ["marianjosephjeffrey", "marianjosephjeffrey.github.io"];

  try {
    const response = await fetch(apiUrl);
    const projects = await response.json();

    const projectContainer = document.getElementById("projects");
    console.log("🧱 Found project container:", projectContainer);

    for (const project of projects) {
      // Skip excluded repos
      if (excludedRepos.includes(project.name)) continue;

      const projectCard = document.createElement("div");
      projectCard.classList.add("project-card");

      const detailsUrl = `https://raw.githubusercontent.com/${username}/${project.name}/main/details.md`;
      let detailsContent = "<em>No details available.</em>";

      try {
        const detailsResponse = await fetch(detailsUrl);
        if (detailsResponse.ok) {
          const rawMarkdown = await detailsResponse.text();
          detailsContent = marked.parse(rawMarkdown); // Convert Markdown to HTML
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