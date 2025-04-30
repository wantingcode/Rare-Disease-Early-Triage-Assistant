let awaitingAnswer = false;

function appendUserMessage(message) {
  const chatBox = document.getElementById('chat-box');
  const bubble = document.createElement('div');
  bubble.className = 'chat-bubble user';
  bubble.textContent = message;
  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function appendQuestion(question) {
  const chatBox = document.getElementById('chat-box');
  const bubble = document.createElement('div');
  bubble.className = 'chat-bubble assistant';
  bubble.innerHTML = `${question}<br>
    <button onclick="sendAnswer('yes')">✅ 是</button>
    <button onclick="sendAnswer('no')">❌ 否</button>`;
  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function appendFinalDiagnosis(diagnosis) {
  const chatBox = document.getElementById('chat-box');
  const bubble = document.createElement('div');
  bubble.className = 'chat-bubble assistant';
  bubble.innerHTML = `<strong>✅ 初步诊断：</strong> ${diagnosis}`;
  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function appendHospitals(hospitals) {
  const modulesList = document.getElementById('modules-list');
  modulesList.innerHTML = ''; // 清空上一次的推荐
  hospitals.forEach(hospital => {
    const li = document.createElement('li');
    li.innerHTML = `
      <strong>${hospital.name_zh} (${hospital.name_en})</strong><br>
      📍 ${hospital.address_zh} / ${hospital.address_en}<br>
      🏥 ${hospital.specialty_zh} / ${hospital.specialty_en}
    `;
    modulesList.appendChild(li);
  });
}

function sendMessage() {
  const input = document.getElementById('user-input');
  const message = input.value.trim();
  if (!message) return;

  appendUserMessage(message);  // ✅ 发送前先自己显示气泡！

  input.value = '';
  showLoading();

  fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  })
  .then(response => response.json())
  .then(data => {
    hideLoading();
    if (data.question) {
      appendQuestion(data.question);
      awaitingAnswer = true;
    }
    if (data.final_disease) {
      appendFinalDiagnosis(data.final_disease);
    }
    if (data.hospitals && data.hospitals.length > 0) {
      appendHospitals(data.hospitals);
    }
  });
}

function sendAnswer(answer) {
  showLoading();
  fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ answer })
  })
  .then(response => response.json())
  .then(data => {
    console.log("🧪 接收到服务器响应:", data);  // ✅ 这一行
    
    hideLoading();
    if (data.question) {
      appendQuestion(data.question);
      awaitingAnswer = true;
    }
    if (data.final_disease) {
      appendFinalDiagnosis(data.final_disease);
    }
    if (data.hospitals && data.hospitals.length > 0) {
      appendHospitals(data.hospitals);
    }
  });
}

function showLoading() {
  document.getElementById('loading').style.display = 'block';
}

function hideLoading() {
  document.getElementById('loading').style.display = 'none';
}

function appendHospitals(hospitals) {
  const hospitalList = document.getElementById('hospitals-list');
  if (!hospitalList) {
    console.error("❌ #hospitals-list not found in DOM");
    return;
  }

  hospitalList.innerHTML = ''; // 清空旧内容

  hospitals.forEach(h => {
    hospitalList.innerHTML += `
      <li class="hospital-item">
        <strong>${h.name_zh} (${h.name_en})</strong><br>
        📍 ${h.address_zh} / ${h.address_en}<br>
        🏥 ${h.specialty_zh} / ${h.specialty_en}
      </li>
    `;
  });

  console.log("✅ 推荐医院渲染完成");
}