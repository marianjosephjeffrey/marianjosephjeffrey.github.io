document.addEventListener("DOMContentLoaded", async function () {
  const username = "marianjosephjeffrey";
  const ctfRepos = {
    "2023-NCL-CTF": {
      rank: "34 / 302",
      top: "Top 11%"
    },
    "2024-NCL-CTF": {
      rank: "1038 / 8487",
      top: "Top 12%"
    }
  };

  const apiUrl = `https://api.github.com/users/${username}/repos`;

  try {
    const response = await fetch(apiUrl);
    const repos = await response.json();

    const ctfContainer = document.getElementById("ctf-projects");

    for (const project of repos) {
      if (!ctfRepos.hasOwnProperty(project.name)) continue;

      const { rank, top } = ctfRepos[project.name];

      const projectCard = document.createElement("div");
      projectCard.classList.add("project-card");

      projectCard.innerHTML = `
        <div class="project-details">
          <h3>${project.name.replace(/-/g, " ")}</h3>
          <p><strong>Rank:</strong> ${rank}</p>
          <p><strong>Performance:</strong> ${top}</p>
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