// ============================================================
// quiz-engine.js — Motor de Quiz para School v4
// Conecta el banco de preguntas con la interfaz
// ============================================================

(function() {
  'use strict';

  // ── Estado del quiz ──
  let quizActual = {
    materia: null,
    preguntas: [],
    indice: 0,
    aciertos: 0,
    fallos: 0,
    respondida: false
  };

  // ── Mapeo de botones de materia → clave en PREGUNTAS ──
  const MATERIAS_MAP = {
    'matematicas':  { clave: 'matematicas',  nombre: '📐 Matemáticas',            emoji: '📐' },
    'lengua':       { clave: 'lengua',       nombre: '📖 Lengua Castellana',       emoji: '📖' },
    'naturales':    { clave: 'naturales',     nombre: '🌿 Ciencias Naturales',      emoji: '🌿' },
    'sociales':     { clave: 'sociales',      nombre: '🌍 Ciencias Sociales',       emoji: '🌍' },
    'ingles':       { clave: 'ingles',        nombre: '🇬🇧 Inglés',                emoji: '🇬🇧' },
    'artistica':    { clave: 'artistica',     nombre: '🎨 Educación Artística',     emoji: '🎨' },
    'valores':      { clave: 'valores',       nombre: '🤝 Valores Cívicos',         emoji: '🤝' }
  };

  // ── Barajar array (Fisher-Yates) ──
  function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  // ── Iniciar quiz de una materia ──
  window.iniciarQuiz = function(materiaKey, numPreguntas = 10) {
    const config = MATERIAS_MAP[materiaKey];
    if (!config) {
      console.error('Materia no encontrada:', materiaKey);
      alert('❌ Materia no encontrada: ' + materiaKey);
      return;
    }

    if (typeof PREGUNTAS === 'undefined' || !PREGUNTAS[config.clave]) {
      console.error('Banco de preguntas no cargado o materia sin preguntas');
      alert('❌ No se encontraron preguntas. Verifica que preguntas.js está cargado.');
      return;
    }

    const todas = PREGUNTAS[config.clave];
    if (todas.length === 0) {
      alert('❌ No hay preguntas para ' + config.nombre);
      return;
    }

    // Seleccionar y barajar preguntas
    const seleccionadas = shuffle(todas).slice(0, Math.min(numPreguntas, todas.length));

    quizActual = {
      materia: config,
      preguntas: seleccionadas,
      indice: 0,
      aciertos: 0,
      fallos: 0,
      respondida: false
    };

    mostrarSeccion('quiz-container');
    renderPregunta();
  };

  // ── Renderizar pregunta actual ──
  function renderPregunta() {
    const container = document.getElementById('quiz-container');
    if (!container) {
      console.error('No se encontró #quiz-container en el HTML');
      return;
    }

    const q = quizActual.preguntas[quizActual.indice];
    const total = quizActual.preguntas.length;
    const num = quizActual.indice + 1;
    quizActual.respondida = false;

    container.innerHTML = `
      <div class="quiz-wrapper">
        <div class="quiz-header">
          <h2>${quizActual.materia.emoji} ${quizActual.materia.nombre}</h2>
          <div class="quiz-progress">
            <span>Pregunta ${num} de ${total}</span>
            <div class="progress-bar">
              <div class="progress-fill" style="width: ${(num/total)*100}%"></div>
            </div>
          </div>
          <div class="quiz-score">
            ✅ ${quizActual.aciertos} &nbsp; ❌ ${quizActual.fallos}
          </div>
        </div>

        <div class="quiz-question">
          <p class="pregunta-texto">${q.pregunta}</p>
        </div>

        <div class="quiz-options" id="quiz-options">
          ${q.opciones.map((op, i) => `
            <button class="quiz-option-btn" data-index="${i}" onclick="seleccionarRespuesta(${i})">
              <span class="option-letter">${String.fromCharCode(65+i)}</span>
              <span class="option-text">${op}</span>
            </button>
          `).join('')}
        </div>

        <div class="quiz-feedback" id="quiz-feedback" style="display:none;"></div>

        <div class="quiz-actions" id="quiz-actions" style="display:none;">
          <button class="btn-siguiente" onclick="siguientePregunta()">
            ${num < total ? 'Siguiente ➡️' : 'Ver Resultados 🏆'}
          </button>
        </div>
      </div>
    `;
  }

  // ── Seleccionar respuesta ──
  window.seleccionarRespuesta = function(indice) {
    if (quizActual.respondida) return;
    quizActual.respondida = true;

    const q = quizActual.preguntas[quizActual.indice];
    const esCorrecta = (indice === q.correcta);
    const botones = document.querySelectorAll('.quiz-option-btn');
    const feedback = document.getElementById('quiz-feedback');
    const actions = document.getElementById('quiz-actions');

    // Marcar botones
    botones.forEach((btn, i) => {
      btn.disabled = true;
      btn.style.pointerEvents = 'none';
      if (i === q.correcta) {
        btn.classList.add('correct');
        btn.style.background = '#d4edda';
        btn.style.borderColor = '#28a745';
      }
      if (i === indice && !esCorrecta) {
        btn.classList.add('incorrect');
        btn.style.background = '#f8d7da';
        btn.style.borderColor = '#dc3545';
      }
    });

    // Actualizar puntuación
    if (esCorrecta) {
      quizActual.aciertos++;
      feedback.innerHTML = `<div class="feedback-correct">✅ ¡Correcto! ${q.explicacion}</div>`;
    } else {
      quizActual.fallos++;
      feedback.innerHTML = `<div class="feedback-incorrect">❌ Incorrecto. ${q.explicacion}</div>`;
    }

    feedback.style.display = 'block';
    actions.style.display = 'flex';

    // Guardar progreso en localStorage
    guardarProgreso(quizActual.materia.clave, esCorrecta);
  };

  // ── Siguiente pregunta ──
  window.siguientePregunta = function() {
    quizActual.indice++;
    if (quizActual.indice < quizActual.preguntas.length) {
      renderPregunta();
    } else {
      mostrarResultados();
    }
  };

  // ── Mostrar resultados finales ──
  function mostrarResultados() {
    const container = document.getElementById('quiz-container');
    const total = quizActual.preguntas.length;
    const nota = Math.round((quizActual.aciertos / total) * 10);
    const porcentaje = Math.round((quizActual.aciertos / total) * 100);

    let emoji, mensaje;
    if (nota >= 9) { emoji = '🏆'; mensaje = '¡Sobresaliente! ¡Eres un crack!'; }
    else if (nota >= 7) { emoji = '🌟'; mensaje = '¡Notable! ¡Muy bien hecho!'; }
    else if (nota >= 5) { emoji = '👍'; mensaje = '¡Aprobado! Sigue practicando.'; }
    else { emoji = '💪'; mensaje = 'Necesitas repasar. ¡Tú puedes!'; }

    container.innerHTML = `
      <div class="quiz-results">
        <h2>${emoji} Resultados — ${quizActual.materia.nombre}</h2>
        <div class="results-score">
          <div class="nota-grande">${nota}/10</div>
          <p>${porcentaje}% de aciertos</p>
        </div>
        <div class="results-detail">
          <p>✅ Aciertos: <strong>${quizActual.aciertos}</strong></p>
          <p>❌ Fallos: <strong>${quizActual.fallos}</strong></p>
          <p>📝 Total: <strong>${total}</strong> preguntas</p>
        </div>
        <p class="results-message">${mensaje}</p>
        <div class="results-actions">
          <button class="btn-repetir" onclick="iniciarQuiz('${quizActual.materia.clave}')">
            🔄 Repetir Quiz
          </button>
          <button class="btn-volver" onclick="mostrarSeccion('materias')">
            📚 Elegir otra materia
          </button>
          <button class="btn-volver" onclick="mostrarSeccion('inicio')">
            🏠 Inicio
          </button>
        </div>
      </div>
    `;

    // Guardar resultado completo
    guardarResultadoExamen(quizActual.materia.clave, quizActual.aciertos, total);
  }

  // ── Guardar progreso en localStorage ──
  function guardarProgreso(materia, acierto) {
    try {
      const key = 'school_v4_progreso';
      const data = JSON.parse(localStorage.getItem(key) || '{}');
      if (!data[materia]) data[materia] = { total: 0, aciertos: 0 };
      data[materia].total++;
      if (acierto) data[materia].aciertos++;
      localStorage.setItem(key, JSON.stringify(data));
    } catch(e) { console.warn('No se pudo guardar progreso:', e); }
  }

  function guardarResultadoExamen(materia, aciertos, total) {
    try {
      const key = 'school_v4_examenes';
      const data = JSON.parse(localStorage.getItem(key) || '[]');
      data.push({
        materia: materia,
        aciertos: aciertos,
        total: total,
        nota: Math.round((aciertos/total)*10),
        fecha: new Date().toISOString()
      });
      localStorage.setItem(key, JSON.stringify(data));
    } catch(e) { console.warn('No se pudo guardar examen:', e); }
  }

  // ── Función auxiliar para mostrar secciones ──
  window.mostrarSeccion = window.mostrarSeccion || function(seccionId) {
    document.querySelectorAll('.section, .page, [data-section]').forEach(el => {
      el.style.display = 'none';
    });
    const target = document.getElementById(seccionId);
    if (target) target.style.display = 'block';
  };

  // ── Registrar event listeners en botones de materia ──
  document.addEventListener('DOMContentLoaded', function() {
    // Buscar botones de materia por data-materia o por clase
    document.querySelectorAll('[data-materia]').forEach(btn => {
      btn.addEventListener('click', function() {
        const materia = this.getAttribute('data-materia');
        iniciarQuiz(materia);
      });
    });

    // También buscar por onclick existentes que llamen a funciones de quiz
    console.log('✅ Quiz Engine cargado — ' + Object.keys(MATERIAS_MAP).length + ' materias disponibles');
    console.log('📊 Preguntas cargadas:', Object.keys(PREGUNTAS || {}).map(k => k + ': ' + (PREGUNTAS[k]||[]).length).join(', '));
  });

})();
