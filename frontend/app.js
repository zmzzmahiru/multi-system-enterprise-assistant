const API_URL = "http://127.0.0.1:8000/query";

const form = document.querySelector("#query-form");
const input = document.querySelector("#query-input");
const workflowEl = document.querySelector("#workflow");
const resultEl = document.querySelector("#result");
const submitButton = form.querySelector("button");

const fieldLabels = {
  summary: "Summary",
  first_week_tasks: "First Week Tasks",
  documents_to_read: "Documents To Read",
  people_to_contact: "People To Contact",
  meetings: "Meetings",
  completed_work: "Completed Work",
  blockers: "Blockers",
  owners: "Owners",
  next_steps: "Next Steps",
  sources: "Sources",
};

function formatLabel(key) {
  return fieldLabels[key] || key.replaceAll("_", " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function renderList(items) {
  const list = document.createElement("ul");
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    list.appendChild(li);
  });
  return list;
}

function renderObject(value) {
  const wrapper = document.createElement("div");
  wrapper.className = "kv-list";

  Object.entries(value).forEach(([key, item]) => {
    const row = document.createElement("div");
    row.className = "kv-row";

    const name = document.createElement("span");
    name.textContent = formatLabel(key);

    const count = document.createElement("strong");
    count.textContent = item;

    row.append(name, count);
    wrapper.appendChild(row);
  });

  return wrapper;
}

function renderValue(value) {
  if (Array.isArray(value)) {
    return renderList(value);
  }

  if (value && typeof value === "object") {
    return renderObject(value);
  }

  const paragraph = document.createElement("p");
  paragraph.textContent = value ?? "";
  return paragraph;
}

function renderResponse(data) {
  workflowEl.textContent = data.workflow || "Needs clarification";
  resultEl.className = "result";
  resultEl.replaceChildren();

  Object.entries(data)
    .filter(([key]) => key !== "workflow")
    .forEach(([key, value]) => {
      const section = document.createElement("section");
      section.className = "field";

      const heading = document.createElement("h2");
      heading.textContent = formatLabel(key);

      section.append(heading, renderValue(value));
      resultEl.appendChild(section);
    });
}

function renderError(message) {
  workflowEl.textContent = "Error";
  resultEl.className = "result error";
  resultEl.textContent = message;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const query = input.value.trim();
  if (!query) {
    return;
  }

  submitButton.disabled = true;
  submitButton.textContent = "Sending";
  workflowEl.textContent = "Loading";
  resultEl.className = "result empty";
  resultEl.textContent = "Waiting for response...";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    renderResponse(await response.json());
  } catch (error) {
    renderError(error.message || "Unable to reach the backend.");
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Submit";
  }
});
