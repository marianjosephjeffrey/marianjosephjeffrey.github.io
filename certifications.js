document.addEventListener("DOMContentLoaded", async function () {
  const username = "marianjosephjeffrey";
  const ctfRepos = ["2023-NCL-CTF", "2024-NCL-CTF"];
  const apiUrl = `https://api.github.com/users/${username}/repos`;

  try {
    const response = await fetch(apiUrl);
    const repos = await response.json();

    const ctfContainer = document.getElementById("ctf-projects");

    for (const project of repos) {
      if (!ctfRepos.includes(project.name)) continue;

      const projectCard = document.createElement("div");
      projectCard.classList.add("project-card");

      const createdDate = new Date(project.created_at);
      const updatedDate = new Date(project.updated_at);
      const duration = Math.round(
        (updatedDate - createdDate) / (1000 * 60 * 60 * 24)
      );

      projectCard.innerHTML = `
        <div class="project-details">
          <h3>${project.name.replace(/-/g, " ")}</h3>
          <p><strong>Duration:</strong> ${duration} days</p>
        </div>
        <div class="project-links">
          <a href="${project.html_url}" target="_blank" class="github-link">View on GitHub</a>
        </div>
      `;

      ctfContainer.appendChild(projectCard);
    }
  } catch (error) {
    console.error("Error loading CTF repos:", error);
  }
});
