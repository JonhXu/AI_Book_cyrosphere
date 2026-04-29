let currentMode = "classroom";
let currentQuiz = null;
const API_BASE =
  localStorage.getItem("CRYOSPHERE_API_BASE") ||
  (window.location.protocol === "file:" ? "http://127.0.0.1:8000" : "");
const STATIC_MODE = isGithubPages() && !localStorage.getItem("CRYOSPHERE_API_BASE");

const questionInput = document.querySelector("#question");
const askButton = document.querySelector("#askButton");
const answerBody = document.querySelector("#answerBody");
const citationList = document.querySelector("#citationList");
const errorBox = document.querySelector("#errorBox");
const indexStatus = document.querySelector("#indexStatus");
const quizForm = document.querySelector("#quizForm");
const quizTitle = document.querySelector("#quizTitle");
const quizDescription = document.querySelector("#quizDescription");
const quizResult = document.querySelector("#quizResult");
const submitQuizButton = document.querySelector("#submitQuizButton");
const chaptersTitle = document.querySelector("#chaptersTitle");
const chaptersDescription = document.querySelector("#chaptersDescription");
const chapterList = document.querySelector("#chapterList");
const conceptsTitle = document.querySelector("#conceptsTitle");
const conceptsDescription = document.querySelector("#conceptsDescription");
const conceptList = document.querySelector("#conceptList");
const teacherMetrics = document.querySelector("#teacherMetrics");
const learningRecords = document.querySelector("#learningRecords");
const frequentQuestions = document.querySelector("#frequentQuestions");

document.querySelectorAll(".mode-button").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".mode-button").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    currentMode = button.dataset.mode;
  });
});

document.querySelectorAll(".nav-item").forEach((button) => {
  button.addEventListener("click", () => switchView(button.dataset.view));
});

askButton.addEventListener("click", ask);
document.querySelector("#refreshChaptersButton").addEventListener("click", loadChapters);
document.querySelector("#refreshConceptsButton").addEventListener("click", loadConcepts);
document.querySelector("#reloadQuizButton").addEventListener("click", loadQuiz);
submitQuizButton.addEventListener("click", submitQuiz);
document.querySelector("#refreshTeacherButton").addEventListener("click", loadTeacherDashboard);

questionInput.addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
    ask();
  }
});

loadIndexStatus();
loadChapters();
loadConcepts();
loadQuiz();
loadTeacherDashboard();

function switchView(view) {
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.toggle("active", item.dataset.view === view);
  });
  document.querySelectorAll(".view").forEach((section) => {
    section.classList.toggle("active", section.id === `view-${view}`);
  });

  if (view === "teacher") {
    loadTeacherDashboard();
  }
  if (view === "chapters" && !chapterList.innerHTML.trim()) {
    loadChapters();
  }
  if (view === "concepts" && !conceptList.innerHTML.trim()) {
    loadConcepts();
  }
  if (view === "quiz" && !currentQuiz) {
    loadQuiz();
  }
}

async function loadIndexStatus() {
  if (STATIC_MODE) {
    indexStatus.textContent = "GitHub Pages 静态演示已加载；完整问答需连接公网后端 API。";
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/api/index/status`);
    const data = await response.json();
    indexStatus.textContent = `${data.message}，共 ${data.chunk_count} 个知识块。`;
  } catch {
    indexStatus.textContent = isGithubPages()
      ? "GitHub Pages 静态演示已加载；完整问答需连接公网后端 API。"
      : "暂时无法读取知识库状态。";
  }
}

async function ask() {
  const question = questionInput.value.trim();
  if (!question) return;

  if (STATIC_MODE) {
    errorBox.hidden = true;
    answerBody.textContent = buildStaticAnswer(question);
    renderCitations([
      {
        chunk_id: "static-demo-1",
        page: 261,
        chapter: "第 8 章：冰冻圈与其他圈层的相互作用",
        text: "静态演示引用：冰冻圈通过高反照率、相变潜热和低导热性等特征影响气候系统。部署公网 FastAPI 后端后，这里会显示真实教材检索片段。",
        score: null
      },
      {
        chunk_id: "static-demo-2",
        page: 14,
        chapter: "第 1 章：冰冻圈与冰冻圈科学",
        text: "静态演示引用：冰冻圈科学关注冰、雪、冻土等组成要素及其与气候变化、社会发展的关系。",
        score: null
      }
    ]);
    loadTeacherDashboard();
    return;
  }

  askButton.disabled = true;
  askButton.textContent = "检索教材中";
  errorBox.hidden = true;
  answerBody.textContent = "正在检索教材并生成回答...";
  citationList.innerHTML = "";

  try {
    const response = await fetch(`${API_BASE}/api/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, mode: currentMode, top_k: 5 })
    });

    if (!response.ok) {
      throw new Error(`请求失败：${response.status}`);
    }

    const data = await response.json();
    answerBody.textContent = data.answer;
    renderCitations(data.citations);
    loadTeacherDashboard();
  } catch (error) {
    errorBox.hidden = false;
    errorBox.textContent = error instanceof Error ? error.message : "请求失败";
    answerBody.textContent = isGithubPages()
      ? "当前是 GitHub Pages 静态访问模式。页面可以公网打开，但 DeepSeek 问答、学习记录和教师端统计需要 FastAPI 后端部署到公网后才能使用。"
      : "请求失败，请确认后端服务正在运行。";
  } finally {
    askButton.disabled = false;
    askButton.textContent = "提问";
  }
}

function renderCitations(citations) {
  if (!citations.length) {
    citationList.innerHTML = '<p class="muted">暂无引用。</p>';
    return;
  }

  citationList.innerHTML = citations
    .map((citation) => {
      const page = citation.page ?? "?";
      const score = citation.score ? `相关度 ${citation.score}` : "已召回";
      const chapter = citation.chapter ? `<strong>${escapeHtml(citation.chapter)}</strong>` : "";
      return `
        <div class="citation-card">
          <div class="citation-meta">
            <span>第 ${page} 页</span>
            <span>${score}</span>
          </div>
          ${chapter}
          <p>${escapeHtml(citation.text)}</p>
        </div>
      `;
    })
    .join("");
}

async function loadChapters() {
  chapterList.innerHTML = '<p class="muted">正在生成章节学习内容...</p>';
  if (STATIC_MODE) {
    chaptersTitle.textContent = "《冰冻圈科学概论》章节学习路线";
    chaptersDescription.textContent = "按教材 10 章组织学习。当前为 GitHub Pages 静态演示版，部署公网后端后可刷新生成不同学习任务。";
    chapterList.innerHTML = renderStaticChapters();
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/api/learning/chapters`);
    const data = await response.json();
    chaptersTitle.textContent = data.title;
    chaptersDescription.textContent = data.description;
    chapterList.innerHTML = data.chapters.map(renderChapter).join("");
    bindQuickQuestions(chapterList);
  } catch {
    chapterList.innerHTML = isGithubPages()
      ? renderStaticChapters()
      : '<p class="muted">章节学习内容加载失败，请确认后端服务正在运行。</p>';
  }
}

function renderChapter(chapter) {
  const number = String(chapter.number).padStart(2, "0");
  return `
    <article class="chapter-card">
      <div class="chapter-number">${number}</div>
      <div class="chapter-content">
        <div class="chapter-heading">
          <span>${escapeHtml(chapter.pages)}</span>
          <h3>第 ${chapter.number} 章：${escapeHtml(chapter.title)}</h3>
          <p>${escapeHtml(chapter.title_en)}</p>
        </div>
        <p>${escapeHtml(chapter.summary)}</p>
        <div class="learning-task">
          <strong>本次学习任务</strong>
          <span>${escapeHtml(chapter.learning_task)}</span>
        </div>
        <button class="quick-question" data-question="${escapeHtml(chapter.question)}">围绕本章向助教提问</button>
      </div>
    </article>
  `;
}

async function loadConcepts() {
  conceptList.innerHTML = '<p class="muted">正在生成概念卡片...</p>';
  if (STATIC_MODE) {
    conceptsTitle.textContent = "核心概念复习卡片";
    conceptsDescription.textContent = "当前为静态演示概念卡。部署公网后端后可动态刷新不同概念组。";
    conceptList.innerHTML = renderStaticConcepts();
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/api/learning/concepts`);
    const data = await response.json();
    conceptsTitle.textContent = data.title;
    conceptsDescription.textContent = data.description;
    conceptList.innerHTML = data.concepts.map(renderConcept).join("");
    bindQuickQuestions(conceptList);
  } catch {
    conceptList.innerHTML = isGithubPages()
      ? renderStaticConcepts()
      : '<p class="muted">概念卡片加载失败，请确认后端服务正在运行。</p>';
  }
}

function renderConcept(concept) {
  return `
    <article class="concept-card">
      <h3>${escapeHtml(concept.title)}</h3>
      <p>${escapeHtml(concept.summary)}</p>
      <div class="learning-task">
        <strong>复习提示</strong>
        <span>${escapeHtml(concept.review_prompt)}</span>
      </div>
      <button class="quick-question" data-question="${escapeHtml(concept.question)}">向助教追问</button>
    </article>
  `;
}

function bindQuickQuestions(container) {
  container.querySelectorAll(".quick-question").forEach((button) => {
    button.addEventListener("click", () => {
      questionInput.value = button.dataset.question;
      switchView("qa");
    });
  });
}

async function loadQuiz() {
  quizResult.innerHTML = "";
  quizForm.innerHTML = '<p class="muted">正在加载题目...</p>';
  if (STATIC_MODE) {
    currentQuiz = getStaticQuiz();
    quizTitle.textContent = currentQuiz.title;
    quizDescription.textContent = currentQuiz.description;
    quizForm.innerHTML = currentQuiz.questions
      .map((question, index) => renderQuizQuestion(question, index))
      .join("");
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/api/quiz/current`);
    currentQuiz = await response.json();
    quizTitle.textContent = currentQuiz.title;
    quizDescription.textContent = currentQuiz.description;
    quizForm.innerHTML = currentQuiz.questions
      .map((question, index) => renderQuizQuestion(question, index))
      .join("");
  } catch {
    quizForm.innerHTML = '<p class="muted">测验加载失败；GitHub Pages 静态模式需要公网后端 API 才能生成题组。</p>';
  }
}

function renderQuizQuestion(question, index) {
  return `
    <fieldset class="quiz-question">
      <legend>${index + 1}. ${escapeHtml(question.prompt)}</legend>
      ${question.options
        .map(
          (option) => `
            <label class="choice">
              <input type="radio" name="${escapeHtml(question.id)}" value="${escapeHtml(option)}" />
              <span>${escapeHtml(option)}</span>
            </label>
          `
        )
        .join("")}
    </fieldset>
  `;
}

async function submitQuiz(event) {
  event.preventDefault();
  if (!currentQuiz) return;

  const formData = new FormData(quizForm);
  const answers = {};
  currentQuiz.questions.forEach((question) => {
    answers[question.id] = formData.get(question.id) || "";
  });

  if (STATIC_MODE) {
    renderQuizResult(gradeStaticQuiz(currentQuiz, answers));
    loadTeacherDashboard();
    return;
  }

  submitQuizButton.disabled = true;
  submitQuizButton.textContent = "提交中";
  try {
    const response = await fetch(`${API_BASE}/api/quiz/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ quiz_id: currentQuiz.id, answers })
    });
    const result = await response.json();
    renderQuizResult(result);
    loadTeacherDashboard();
  } catch {
    quizResult.innerHTML = '<div class="error">提交失败，请稍后重试。</div>';
  } finally {
    submitQuizButton.disabled = false;
    submitQuizButton.textContent = "提交测验";
  }
}

function renderQuizResult(result) {
  quizResult.innerHTML = `
    <div class="result-summary">
      <strong>${result.score}/${result.total}</strong>
      <span>得分率 ${result.percent}%</span>
    </div>
    <div class="record-list">
      ${result.items
        .map(
          (item, index) => `
            <div class="record-item ${item.correct ? "correct" : "wrong"}">
              <strong>第 ${index + 1} 题：${item.correct ? "正确" : "需要复习"}</strong>
              <p>正确答案：${escapeHtml(item.correct_answer)}</p>
              <p>${escapeHtml(item.explanation)}</p>
            </div>
          `
        )
        .join("")}
    </div>
  `;
}

async function loadTeacherDashboard() {
  if (STATIC_MODE) {
    renderTeacherMetrics({
      chunk_count: 1384,
      total_questions: 0,
      grounded_rate: 0,
      quiz_attempts: 0,
      average_quiz_percent: 0
    });
    learningRecords.innerHTML = `
      <div class="record-item">
        <strong>GitHub Pages 静态演示模式</strong>
        <p>公网页面已可访问。部署 FastAPI 后端并配置 CRYOSPHERE_API_BASE 后，将显示真实学习记录。</p>
      </div>
    `;
    frequentQuestions.innerHTML = `
      <div class="record-item"><strong>冰冻圈包括哪些组成部分？</strong></div>
      <div class="record-item"><strong>冰冻圈为什么影响气候系统？</strong></div>
      <div class="record-item"><strong>多年冻土退化会带来什么影响？</strong></div>
    `;
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/api/teacher/dashboard`);
    const data = await response.json();
    renderTeacherMetrics(data);
    renderLearningRecords(data.recent_records);
    renderFrequentQuestions(data.frequent_questions);
  } catch {
    teacherMetrics.innerHTML = '<div class="error">教师端数据读取失败。</div>';
  }
}

function isGithubPages() {
  return window.location.hostname.endsWith("github.io");
}

function buildStaticAnswer(question) {
  return `这是 GitHub Pages 静态演示回答。\n\n你的问题是：“${question}”\n\n在完整版本中，系统会先检索《冰冻圈科学概论》教材知识库，再调用 DeepSeek V4 生成带教材出处的中文回答。当前公网静态页不能直接保存 DeepSeek API Key，也不能运行 FastAPI/SQLite 后端，所以这里展示的是演示回答。\n\n要启用完整问答，需要把 FastAPI 后端部署到公网，并在浏览器 localStorage 中设置 CRYOSPHERE_API_BASE 为后端地址。`;
}

function renderStaticChapters() {
  const chapters = [
    ["01", "冰冻圈与冰冻圈科学", "介绍冰冻圈的定义、研究对象和学科意义。"],
    ["02", "冰冻圈的分类与地理分布", "梳理陆地、海洋和大气冰冻圈的分类及全球分布。"],
    ["03", "冰冻圈的形成与发育", "解释冰冻圈要素形成、发育和演化的基本过程。"],
    ["04", "冰冻圈的物理性质", "理解冰雪冻土的热学、力学、光学和电磁性质。"],
    ["05", "冰冻圈的化学特征", "认识冰川雪冰、冻土和海冰中的化学信息。"],
    ["06", "冰冻圈中的气候与环境记录", "学习冰芯、冻土等载体如何保存环境记录。"],
    ["07", "不同时间尺度上的冰冻圈演化", "比较地质时期和现代冰冻圈变化。"],
    ["08", "冰冻圈与其他圈层的相互作用", "理解冰冻圈与大气圈、水圈、生物圈、岩石圈的反馈。"],
    ["09", "冰冻圈变化影响、适应与可持续发展", "关注灾害、工程、水资源和社会经济影响。"],
    ["10", "冰冻圈科学野外观测与测量", "了解观测、实验和数据获取方法。"]
  ];
  return chapters
    .map(
      ([number, title, summary]) => `
        <article class="chapter-card">
          <div class="chapter-number">${number}</div>
          <div class="chapter-content">
            <div class="chapter-heading">
              <h3>第 ${Number(number)} 章：${title}</h3>
            </div>
            <p>${summary}</p>
            <div class="learning-task">
              <strong>静态演示</strong>
              <span>连接公网后端 API 后可刷新生成本章学习任务。</span>
            </div>
          </div>
        </article>
      `
    )
    .join("");
}

function renderStaticConcepts() {
  return ["冰冻圈", "反照率反馈", "多年冻土", "冰芯记录"]
    .map(
      (title) => `
        <article class="concept-card">
          <h3>${title}</h3>
          <p>这是 GitHub Pages 静态演示卡片。连接公网后端 API 后可刷新生成更多概念复习内容。</p>
        </article>
      `
    )
    .join("");
}

function getStaticQuiz() {
  return {
    id: "static-cryosphere-basics",
    title: "冰冻圈科学基础小测",
    description: "GitHub Pages 静态演示题组，可直接作答并在前端判分。",
    questions: [
      {
        id: "q1",
        prompt: "冰冻圈的主要组成部分不包括哪一项？",
        options: ["冰盖和山地冰川", "积雪和海冰", "多年冻土和季节冻土", "平流层臭氧"],
        answer: "平流层臭氧",
        explanation: "冰冻圈主要关注冰、雪、冻土等固态水圈要素。"
      },
      {
        id: "q2",
        prompt: "为什么说冰冻圈是气候变化的天然指示器？",
        options: ["因为冰冻圈对气候变化敏感", "因为冰冻圈完全不变", "因为冰冻圈只存在于城市", "因为冰冻圈不受温度影响"],
        answer: "因为冰冻圈对气候变化敏感",
        explanation: "冰川、积雪、海冰和冻土等要素会快速响应温度和水分条件变化。"
      },
      {
        id: "q3",
        prompt: "冰雪高反照率主要影响哪一过程？",
        options: ["地表能量平衡", "地核温度", "股票价格", "城市人口密度"],
        answer: "地表能量平衡",
        explanation: "冰雪通过反射太阳辐射改变地表吸收能量。"
      }
    ]
  };
}

function gradeStaticQuiz(quiz, answers) {
  const items = quiz.questions.map((question) => {
    const correct = answers[question.id] === question.answer;
    return {
      question_id: question.id,
      correct,
      correct_answer: question.answer,
      explanation: question.explanation
    };
  });
  const score = items.filter((item) => item.correct).length;
  const total = items.length;
  return {
    quiz_id: quiz.id,
    score,
    total,
    percent: total ? Math.round((score / total) * 1000) / 10 : 0,
    items
  };
}

function renderTeacherMetrics(data) {
  const metrics = [
    ["教材知识块", data.chunk_count],
    ["学生提问数", data.total_questions],
    ["有依据回答率", `${data.grounded_rate}%`],
    ["测验提交次数", data.quiz_attempts],
    ["平均测验得分", `${data.average_quiz_percent}%`]
  ];

  teacherMetrics.innerHTML = metrics
    .map(
      ([label, value]) => `
        <article class="metric-card">
          <span>${label}</span>
          <strong>${value}</strong>
        </article>
      `
    )
    .join("");
}

function renderLearningRecords(records) {
  if (!records.length) {
    learningRecords.innerHTML = '<p class="muted">暂无学习记录。学生提问后会自动生成。</p>';
    return;
  }
  learningRecords.innerHTML = records
    .map(
      (record) => `
        <div class="record-item">
          <strong>${escapeHtml(record.question)}</strong>
          <p>${formatMode(record.mode)} · ${record.grounded ? "已找到教材依据" : "教材依据不足"} · ${escapeHtml(record.created_at)}</p>
          <p>引用页码：${record.citation_pages.length ? record.citation_pages.join("、") : "无"}</p>
        </div>
      `
    )
    .join("");
}

function renderFrequentQuestions(questions) {
  if (!questions.length) {
    frequentQuestions.innerHTML = '<p class="muted">暂无问题记录。</p>';
    return;
  }
  frequentQuestions.innerHTML = questions
    .map((question) => `<div class="record-item"><strong>${escapeHtml(question)}</strong></div>`)
    .join("");
}

function formatMode(mode) {
  return {
    classroom: "课堂解释",
    review: "复习重点",
    homework_hint: "作业提示"
  }[mode] || mode;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
