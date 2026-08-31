const state = {

  classes:
    [],

  // groups:
  //   [],

  subjects:
    [],

  chapters:
    [],


  selectedClass:
    null,

  // selectedGroup:
  //   null,

  selectedSubject:
    null,

  selectedChapter:
    null,


  mode:
    null,


  difficulty:
    "Medium",


  activeQuestion:
    null,

};


const els = {

  classSelect:
    document.getElementById(
      "class-select"
    ),


  // groupSection:
  //   document.getElementById(
  //     "group-section"
  //   ),


  // groupSelect:
  //   document.getElementById(
  //     "group-select"
  //   ),


  // groupProgress:
  //   document.getElementById(
  //     "group-progress"
  //   ),


  subjectSelect:
    document.getElementById(
      "subject-select"
    ),


  chapterSelect:
    document.getElementById(
      "chapter-select"
    ),


  modeTabs:
    document.querySelectorAll(
      ".mode-tab"
    ),


  main:
    document.getElementById(
      "main-panel"
    ),


  progressDots:
    document.querySelectorAll(
      ".progress-dot"
    ),

};


const PART_LABELS = {

  ka:
    "ক",

  kha:
    "খ",

  ga:
    "গ",

  gha:
    "ঘ",

};


const OPTION_LETTERS = [

  "A",

  "B",

  "C",

  "D",

];


const prefersReducedMotion =
  window
    .matchMedia(
      "(prefers-reduced-motion: reduce)"
    )
    .matches;


const MODE_META = {

  qa: {

    title:
      "Ask a Question",

    bn:
      "প্রশ্ন করুন",

    eyebrow:
      "Mode: Ask Question",

  },


  mcq: {

    title:
      "MCQ Practice",

    bn:
      "বহুনির্বাচনি অনুশীলন",

    eyebrow:
      "Mode: MCQ Practice",

  },


  cq: {

    title:
      "Creative Question Practice",

    bn:
      "সৃজনশীল প্রশ্ন অনুশীলন",

    eyebrow:
      "Mode: CQ Practice",

  },

};

// init();
document.addEventListener("DOMContentLoaded", () => {
    init(); 
});


async function init() {

  bindModeTabs();

  bindSelectors();

  renderMain();


  try {

    const {
      classes
    } =
      await Api.getClasses();


    state.classes =
      classes;


    fillSelect(
      els.classSelect,
      classes,
      "Select a class"
    );


    els.classSelect.disabled =
      false;

  } catch (
    err
  ) {

    console.error(
      err
    );


    resetSelect(
      els.classSelect,
      "Curriculum data unavailable"
    );

  }

}


// function requiresGroup(
//   cls
// ) {

//   return (

//     cls ===
//       "Class 9"

//     ||

//     cls ===
//       "Class 10"

//   );

// }


function bindSelectors() {


  els.classSelect?.addEventListener(
    "change",
    async (
      e
    ) => {


      state.selectedClass =
        e.target.value
        ||
        null;


      // state.selectedGroup =
      //   null;


      state.selectedSubject =
        null;


      state.selectedChapter =
        null;


      // state.groups =
      //   [];


      state.subjects =
        [];


      state.chapters =
        [];


      // resetSelect(
      //   els.groupSelect,
      //   "Select a group"
      // );


      resetSelect(
        els.subjectSelect,
        "Select a subject"
      );


      resetSelect(
        els.chapterSelect,
        "Select a chapter"
      );


      // const needsGroup =
      //   requiresGroup(
      //     state.selectedClass
      //   );


      // els
      //   .groupSection
      //   .classList
      //   .toggle(
      //     "hidden",
      //     !needsGroup
      //   );


      // els
      //   .groupProgress
      //   .classList
      //   .toggle(
      //     "hidden",
      //     !needsGroup
      //   );


      updateProgressDots();

      renderMain();


      if (
        !state.selectedClass
      ) {

        return;

      }


      try {


        // if (
        //   needsGroup
        // ) {


        //   const {
        //     groups
        //   } =
        //     await Api.getGroups(
        //       state.selectedClass
        //     );


        //   state.groups =
        //     groups;


        //   fillSelect(
        //     els.groupSelect,
        //     groups,
        //     "Select a group"
        //   );


        //   els.groupSelect.disabled =
        //     false;


        //   return;

        // }


        await loadSubjects();


      } catch (
        err
      ) {


        console.error(
          err
        );

        resetSelect(
            els.subjectSelect,
            "Could not load subjects"
        );


        // if (
        //   needsGroup
        // ) {

        //   resetSelect(
        //     els.groupSelect,
        //     "Could not load groups"
        //   );

        // } else {

        //   resetSelect(
        //     els.subjectSelect,
        //     "Could not load subjects"
        //   );

        // }

      }

    }
  );


  // els.groupSelect?.addEventListener(
  //   "change",
  //   async (
  //     e
  //   ) => {


  //     state.selectedGroup =
  //       e.target.value
  //       ||
  //       null;


  //     state.selectedSubject =
  //       null;


  //     state.selectedChapter =
  //       null;


  //     state.subjects =
  //       [];


  //     state.chapters =
  //       [];


  //     resetSelect(
  //       els.subjectSelect,
  //       "Select a subject"
  //     );


  //     resetSelect(
  //       els.chapterSelect,
  //       "Select a chapter"
  //     );


  //     updateProgressDots();

  //     renderMain();


  //     if (
  //       !state.selectedGroup
  //     ) {

  //       return;

  //     }


  //     try {

  //       await loadSubjects();

  //     } catch (
  //       err
  //     ) {

  //       console.error(
  //         err
  //       );


  //       resetSelect(
  //         els.subjectSelect,
  //         "Could not load subjects"
  //       );

  //     }

  //   }
  // );


  els.subjectSelect?.addEventListener(
    "change",
    async (
      e
    ) => {


      state.selectedSubject =
        e.target.value
        ||
        null;


      state.selectedChapter =
        null;


      state.chapters =
        [];


      resetSelect(
        els.chapterSelect,
        "Select a chapter"
      );


      updateProgressDots();

      renderMain();


      if (
        !state.selectedSubject
      ) {

        return;

      }


      try {


        const {
          chapters
        } =
          await Api.getChapters(

            state.selectedClass,

            // state.selectedGroup,

            state.selectedSubject

          );


        state.chapters =
          chapters;


        fillSelect(

          els.chapterSelect,

          [
            "All Chapters",
            ...chapters,
          ],

          "Select a chapter"

        );


        els.chapterSelect.disabled =
          false;


      } catch (
        err
      ) {


        console.error(
          err
        );


        resetSelect(
          els.chapterSelect,
          "Verified chapters are unavailable"
        );

      }

    }
  );


  els.chapterSelect?.addEventListener(
    "change",
    (
      e
    ) => {


      state.selectedChapter =
        e.target.value
        ||
        null;


      updateProgressDots();

      renderMain();

    }
  );

}


async function loadSubjects() {

  els.subjectSelect.disabled =
    true;


  const {
    subjects
  } =
    await Api.getSubjects(

      state.selectedClass,

      // state.selectedGroup

    );


  state.subjects =
    subjects;


  fillSelect(
    els.subjectSelect,
    subjects,
    "Select a subject"
  );


  els.subjectSelect.disabled =
    false;

}


function updateProgressDots() {

  els.progressDots.forEach(
    (
      dot
    ) => {


      const key =
        dot.dataset.key;


      // if (

      //   key ===
      //     "group"

      //   &&

      //   !requiresGroup(
      //     state.selectedClass
      //   )

      // ) {

      //   dot.classList.remove(
      //     "is-done"
      //   );

      //   return;

      // }


      const done =

        (
          key ===
            "class"

          &&

          !!state.selectedClass
        )

        ||

        // (
        //   key ===
        //     "group"

        //   &&

        //   !!state.selectedGroup
        // )

        // ||

        (
          key ===
            "subject"

          &&

          !!state.selectedSubject
        )

        ||

        (
          key ===
            "chapter"

          &&

          !!state.selectedChapter
        );


      dot.classList.toggle(
        "is-done",
        done
      );

    }
  );

}


function bindModeTabs() {

  els.modeTabs.forEach(
    (
      tab
    ) => {


      tab.addEventListener(
        "click",
        () => {


          state.mode =
            tab.dataset.mode;


          state.activeQuestion =
            null;


          els.modeTabs.forEach(
            (
              currentTab
            ) => {


              currentTab.setAttribute(

                "aria-pressed",

                String(
                  currentTab ===
                    tab
                )

              );

            }
          );


          renderMain();

        }
      );

    }
  );

}


function fillSelect(
  selectEl,
  items,
  placeholder
) {

  selectEl.innerHTML =
    "";


  const placeholderOption =
    document.createElement(
      "option"
    );


  placeholderOption.value =
    "";


  placeholderOption.textContent =
    placeholder;


  selectEl.appendChild(
    placeholderOption
  );


  items.forEach(
    (
      item
    ) => {


      const option =
        document.createElement(
          "option"
        );


      option.value =
        item;


      option.textContent =
        item;


      selectEl.appendChild(
        option
      );

    }
  );

}


function resetSelect(
  selectEl,
  placeholder
) {

  selectEl.innerHTML =
    "";


  const option =
    document.createElement(
      "option"
    );


  option.value =
    "";


  option.textContent =
    placeholder;


  selectEl.appendChild(
    option
  );


  selectEl.disabled =
    true;

}


function selectionsReady() {

  if (

    !state.selectedClass

    ||

    !state.selectedSubject

    ||

    !state.selectedChapter

  ) {

    return false;

  }


  // if (

  //   requiresGroup(
  //     state.selectedClass
  //   )

  //   &&

  //   !state.selectedGroup

  // ) {

  //   return false;

  // }


  return true;

}


function renderMain() {

  if (

    !selectionsReady()

    ||

    !state.mode

  ) {

    els.main.innerHTML =
      emptyStateHtml();

    return;

  }


  const meta =
    MODE_META[
      state.mode
    ];


  const crumbs = [

    state.selectedClass,


    // ...(
    //   requiresGroup(
    //     state.selectedClass
    //   )

    //     ? [
    //         state.selectedGroup
    //       ]

    //     : []
    // ),


    state.selectedSubject,


    state.selectedChapter,

  ].filter(
    Boolean
  );


  els.main.innerHTML = `

    <div class="page-header">

      <span class="page-eyebrow">
        ${meta.eyebrow}
      </span>

      <h1 class="page-title">
        ${meta.title}
      </h1>

      <div class="breadcrumb">

        ${
          crumbs
            .map(
              (
                crumb,
                index
              ) =>

                `<span class="breadcrumb-chip">${
                  escapeHtml(
                    crumb
                  )
                }</span>${
                  index <
                  crumbs.length -
                  1

                    ? '<span class="breadcrumb-sep">›</span>'

                    : ""
                }`
            )
            .join(
              ""
            )
        }

      </div>

    </div>


    <div id="mode-body"></div>

  `;


  if (
    state.mode ===
      "qa"
  ) {

    renderQa();

  }


  if (
    state.mode ===
      "mcq"
  ) {

    renderMcq();

  }


  if (
    state.mode ===
      "cq"
  ) {

    renderCq();

  }

}


function emptyStateHtml() {

  const needsSelection =
    !selectionsReady();


  const heading =
    needsSelection

      ? "Pick a class, subject and chapter to begin"

      : "Now choose how you would like to study";


  return `

    <div class="empty-state">

      <svg
        class="empty-illustration"
        viewBox="0 0 120 90"
        fill="none"
      >

        <path
          d="M60 20 L60 78"
          stroke="#C99A3E"
          stroke-width="1.2"
        />

        <path
          d="M60 20 C48 12 26 10 10 15 C8 15.6 7 17 7 19 L7 66 C7 68 8.4 69 10 68.6 C26 64 48 65 60 74 Z"
          fill="#FFFDF7"
          stroke="#0B6E4F"
          stroke-width="1.4"
        />

        <path
          d="M60 20 C72 12 94 10 110 15 C112 15.6 113 17 113 19 L113 66 C113 68 111.6 69 110 68.6 C94 64 72 65 60 74 Z"
          fill="#FFFDF7"
          stroke="#0B6E4F"
          stroke-width="1.4"
        />

        <path
          d="M17 27 C29 23 44 24 53 30"
          stroke="#DDCEAC"
          stroke-width="1.3"
          stroke-linecap="round"
        />

        <path
          d="M17 37 C29 33 44 34 53 40"
          stroke="#DDCEAC"
          stroke-width="1.3"
          stroke-linecap="round"
        />

        <path
          d="M17 47 C29 43 41 44 48 48"
          stroke="#DDCEAC"
          stroke-width="1.3"
          stroke-linecap="round"
        />

        <path
          d="M67 30 C76 24 91 23 103 27"
          stroke="#DDCEAC"
          stroke-width="1.3"
          stroke-linecap="round"
        />

        <path
          d="M67 40 C76 34 91 33 103 37"
          stroke="#DDCEAC"
          stroke-width="1.3"
          stroke-linecap="round"
        />

        <path
          d="M67 48 C74 44 86 43 98 47"
          stroke="#DDCEAC"
          stroke-width="1.3"
          stroke-linecap="round"
        />

        <circle
          cx="90"
          cy="58"
          r="3"
          fill="#A6332B"
        />

      </svg>


      <span class="eyebrow-tag">
        Welcome
      </span>


      <h2>
        ${heading}
      </h2>


      <p class="empty-sub">

        <span class="bn">
          বাম দিকের তালিকা থেকে শ্রেণি, প্রযোজ্য হলে গ্রুপ, বিষয় ও অধ্যায় নির্বাচন করুন।
        </span>

        Then choose a study mode.

      </p>


      <div class="feature-grid">


        <div class="feature-card">

          <div class="feature-icon">

            <svg
              viewBox="0 0 20 20"
              width="15"
              height="15"
              fill="none"
              stroke="currentColor"
              stroke-width="1.6"
            >

              <circle
                cx="10"
                cy="10"
                r="8"
              />

              <path
                d="M7.6 7.5c.3-1.3 1.5-2 2.7-1.8 1.2.2 2 1.1 1.9 2.2-.1 1.2-1.5 1.6-1.9 2.6-.1.4-.2.8-.2 1.2"
                stroke-linecap="round"
              />

              <circle
                cx="10"
                cy="14"
                r="0.6"
                fill="currentColor"
                stroke="none"
              />

            </svg>

          </div>

          <h3>
            Ask Question
          </h3>

          <p>
            Ask questions from the selected textbook chapter.
          </p>

        </div>


        <div class="feature-card">

          <div class="feature-icon">

            <svg
              viewBox="0 0 20 20"
              width="15"
              height="15"
              fill="none"
              stroke="currentColor"
              stroke-width="1.6"
            >

              <rect
                x="2.5"
                y="3"
                width="15"
                height="14"
                rx="1.5"
              />

              <path
                d="M6 7.5h8M6 10.5h8M6 13.5h5"
                stroke-linecap="round"
              />

            </svg>

          </div>

          <h3>
            MCQ Practice
          </h3>

          <p>
            Practice multiple choice questions.
          </p>

        </div>


        <div class="feature-card">

          <div class="feature-icon">

            <svg
              viewBox="0 0 20 20"
              width="15"
              height="15"
              fill="none"
              stroke="currentColor"
              stroke-width="1.6"
            >

              <path
                d="M4 15.5 3.5 17l1.5-.5L14.5 6.9c.5-.5.5-1.3 0-1.8l-.6-.6c-.5-.5-1.3-.5-1.8 0Z"
              />

              <path
                d="M12 5.5l2 2"
              />

            </svg>

          </div>

          <h3>
            CQ Practice
          </h3>

          <p>
            Practice creative questions.
          </p>

        </div>


      </div>

    </div>

  `;

}


function renderQa() {

  const body =
    document.getElementById(
      "mode-body"
    );


  body.innerHTML = `

    <div class="field">

      <label for="qa-input">
        Your question
      </label>

      <textarea
        id="qa-input"
        rows="3"
        placeholder="Type your question about this chapter…"
      ></textarea>

    </div>


    <div class="btn-row">

      <button
        class="btn btn-primary"
        id="qa-submit"
      >
        Ask
      </button>

    </div>


    <div id="qa-status"></div>

    <div id="qa-result"></div>

  `;


  document
    .getElementById(
      "qa-submit"
    )
    .addEventListener(
      "click",
      async () => {


        const question =
          document
            .getElementById(
              "qa-input"
            )
            .value
            .trim();


        if (!question) {

          return;

        }


        const btn =
          document.getElementById(
            "qa-submit"
          );


        const statusEl =
          document.getElementById(
            "qa-status"
          );


        const resultEl =
          document.getElementById(
            "qa-result"
          );


        btn.disabled =
          true;


        statusEl.innerHTML =
          loadingHtml(
            "Retrieving passages and generating an answer…"
          );


        resultEl.innerHTML =
          "";


        try {


          const res =
            await Api.askQuestion({

              class:
                state.selectedClass,

              // group:
              //   state.selectedGroup,

              subject:
                state.selectedSubject,

              chapter:
                state.selectedChapter,

              question,

            });


          statusEl.innerHTML =
            "";


          resultEl.innerHTML = `

            <div class="answer-block">

              <p>
                ${escapeHtml(
                  res.answer
                )}
              </p>

              <div class="sources">

                ${
                  res.sources
                    .map(
                      (
                        source
                      ) =>

                        `<span class="source-chip">${
                          escapeHtml(
                            source.chapter
                          )
                        } · ${
                          escapeHtml(
                            source.chunk_id
                          )
                        }</span>`
                    )
                    .join(
                      ""
                    )
                }

              </div>

            </div>

          `;


        } catch (
          err
        ) {


          statusEl.innerHTML =
            errorHtml(
              "Could not get an answer. Please try again."
            );


          console.error(
            err
          );


        } finally {


          btn.disabled =
            false;

        }

      }
    );

}


function renderMcq() {

  const body =
    document.getElementById(
      "mode-body"
    );


  body.innerHTML = `

    ${difficultyFieldHtml()}


    <div class="btn-row">

      <button
        class="btn btn-primary"
        id="mcq-generate"
      >
        Generate Question
      </button>

    </div>


    <div id="mcq-status"></div>

    <div id="mcq-question-area"></div>

  `;


  bindDifficultyField();


  document
    .getElementById(
      "mcq-generate"
    )
    .addEventListener(
      "click",
      generateMcqQuestion
    );

}


async function generateMcqQuestion() {

  const btn =
    document.getElementById(
      "mcq-generate"
    );


  const statusEl =
    document.getElementById(
      "mcq-status"
    );


  const area =
    document.getElementById(
      "mcq-question-area"
    );


  btn.disabled =
    true;


  statusEl.innerHTML =
    loadingHtml(
      "Generating a question…"
    );


  area.innerHTML =
    "";


  try {


    const res =
      await Api.generateMcq({

        class:
          state.selectedClass,

        // group:
        //   state.selectedGroup,

        subject:
          state.selectedSubject,

        chapter:
          state.selectedChapter,

        difficulty:
          state.difficulty,

      });


    state.activeQuestion =
      res;


    statusEl.innerHTML =
      "";


    area.innerHTML = `

      <div class="mcq-question">

        ${escapeHtml(
          res.question
        )}

      </div>


      <div
        class="mcq-options"
        id="mcq-options"
      >

        ${
          res.options
            .map(
              (
                option,
                index
              ) => `

                <label
                  class="mcq-option"
                  data-option="${escapeHtml(
                    option
                  )}"
                >

                  <input
                    type="radio"
                    name="mcq-choice"
                    value="${escapeHtml(
                      option
                    )}"
                  />

                  <span class="option-badge">
                    ${
                      OPTION_LETTERS[
                        index
                      ]
                      ||
                      index +
                      1
                    }
                  </span>

                  <span>
                    ${escapeHtml(
                      option
                    )}
                  </span>

                </label>

              `
            )
            .join(
              ""
            )
        }

      </div>


      <div class="btn-row">

        <button
          class="btn btn-primary"
          id="mcq-submit"
        >
          Submit Answer
        </button>

      </div>


      <div id="mcq-result"></div>

    `;


    document
      .getElementById(
        "mcq-submit"
      )
      .addEventListener(
        "click",
        submitMcqAnswer
      );


  } catch (
    err
  ) {


    statusEl.innerHTML =
      errorHtml(
        "Could not generate a question."
      );


    console.error(
      err
    );


  } finally {


    btn.disabled =
      false;

  }

}


async function submitMcqAnswer() {

  const selected =
    document.querySelector(
      'input[name="mcq-choice"]:checked'
    );


  if (!selected) {

    return;

  }


  const submitBtn =
    document.getElementById(
      "mcq-submit"
    );


  const resultEl =
    document.getElementById(
      "mcq-result"
    );


  submitBtn.disabled =
    true;


  resultEl.innerHTML =
    loadingHtml(
      "Grading…"
    );


  try {


    const res =
      await Api.gradeMcq({

        question_id:
          state
            .activeQuestion
            .question_id,

        selected_option:
          selected.value,

      });


    document
      .querySelectorAll(
        ".mcq-option"
      )
      .forEach(
        (
          label
        ) => {


          const option =
            label.dataset.option;


          if (
            option ===
            res.correct_option
          ) {

            label.classList.add(
              "is-correct"
            );

          } else if (
            option ===
            selected.value
          ) {

            label.classList.add(
              "is-incorrect"
            );

          }

        }
      );


    resultEl.innerHTML = `

      <div class="grade-report">

        <div class="grade-total">

          <span class="grade-total-badge">
            ${
              res.correct
                ? "✓"
                : "✗"
            }
          </span>

          <span>
            ${
              res.correct
                ? "Correct"
                : "Incorrect"
            }
          </span>

        </div>


        <p
          class="grade-feedback"
          style="margin-top:8px;"
        >
          ${escapeHtml(
            res.feedback
          )}
        </p>

      </div>

    `;


  } catch (
    err
  ) {


    resultEl.innerHTML =
      errorHtml(
        "Could not grade this answer."
      );


    console.error(
      err
    );


  } finally {


    submitBtn.disabled =
      false;

  }

}


function renderCq() {

  const body =
    document.getElementById(
      "mode-body"
    );


  body.innerHTML = `

    ${difficultyFieldHtml()}


    <div class="btn-row">

      <button
        class="btn btn-primary"
        id="cq-generate"
      >
        Generate Question
      </button>

    </div>


    <div id="cq-status"></div>

    <div id="cq-question-area"></div>

  `;


  bindDifficultyField();


  document
    .getElementById(
      "cq-generate"
    )
    .addEventListener(
      "click",
      generateCqQuestion
    );

}


async function generateCqQuestion() {

  const btn =
    document.getElementById(
      "cq-generate"
    );


  const statusEl =
    document.getElementById(
      "cq-status"
    );


  const area =
    document.getElementById(
      "cq-question-area"
    );


  btn.disabled =
    true;


  statusEl.innerHTML =
    loadingHtml(
      "Generating a creative question…"
    );


  area.innerHTML =
    "";


  try {


    const res =
      await Api.generateCq({

        class:
          state.selectedClass,

        // group:
        //   state.selectedGroup,

        subject:
          state.selectedSubject,

        chapter:
          state.selectedChapter,

        difficulty:
          state.difficulty,

      });


    state.activeQuestion =
      res;


    statusEl.innerHTML =
      "";


    const parts = [

      "ka",

      "kha",

      "ga",

      "gha",

    ];


    area.innerHTML = `

      <div class="cq-stimulus">

        ${escapeHtml(
          res.stimulus
        )}

      </div>


      ${
        parts
          .map(
            (
              part
            ) => `

              <div class="cq-part">

                <div class="cq-part-head">

                  <span class="cq-part-badge">
                    ${PART_LABELS[
                      part
                    ]}
                  </span>

                  <div class="cq-part-label">
                    ${escapeHtml(
                      res[
                        part
                      ]
                    )}
                  </div>

                </div>


                <textarea
                  rows="3"
                  id="cq-answer-${part}"
                  placeholder="Write your answer…"
                  oninput="document.getElementById('cq-count-${part}').textContent = this.value.length + ' characters'"
                ></textarea>


                <div
                  class="char-count"
                  id="cq-count-${part}"
                >
                  0 characters
                </div>

              </div>

            `
          )
          .join(
            ""
          )
      }


      <div class="btn-row">

        <button
          class="btn btn-primary"
          id="cq-submit"
        >
          Submit Answers
        </button>

      </div>


      <div id="cq-result"></div>

    `;


    document
      .getElementById(
        "cq-submit"
      )
      .addEventListener(
        "click",
        submitCqAnswers
      );


  } catch (
    err
  ) {


    statusEl.innerHTML =
      errorHtml(
        "Could not generate a question."
      );


    console.error(
      err
    );


  } finally {


    btn.disabled =
      false;

  }

}


async function submitCqAnswers() {

  const parts = [

    "ka",

    "kha",

    "ga",

    "gha",

  ];


  const student_answers =
    {};


  parts.forEach(
    (
      part
    ) => {


      student_answers[
        part
      ] =
        document
          .getElementById(
            `cq-answer-${part}`
          )
          .value
          .trim();

    }
  );


  const submitBtn =
    document.getElementById(
      "cq-submit"
    );


  const resultEl =
    document.getElementById(
      "cq-result"
    );


  submitBtn.disabled =
    true;


  resultEl.innerHTML =
    loadingHtml(
      "Grading…"
    );


  try {


    const res =
      await Api.gradeCq({

        question_id:
          state
            .activeQuestion
            .question_id,

        student_answers,

      });


    resultEl.innerHTML = `

      <div class="grade-report">

        <div class="grade-report-title">
          Grading Report
        </div>


        ${
          parts
            .map(
              (
                part
              ) => `

                <div class="grade-part">

                  <div class="grade-score">
                    ${
                      res[
                        part
                      ].score
                    }
                  </div>

                  <div class="grade-feedback">
                    ${escapeHtml(
                      res[
                        part
                      ].feedback
                    )}
                  </div>

                </div>

              `
            )
            .join(
              ""
            )
        }


        <div class="grade-total">

          <span
            class="grade-total-badge"
            id="cq-total-badge"
          >
            0
          </span>

          <span>
            Total marks
          </span>

        </div>

      </div>

    `;


    animateCountUp(

      document.getElementById(
        "cq-total-badge"
      ),

      res.total,

      700

    );


  } catch (
    err
  ) {


    resultEl.innerHTML =
      errorHtml(
        "Could not grade these answers."
      );


    console.error(
      err
    );


  } finally {


    submitBtn.disabled =
      false;

  }

}


function animateCountUp(
  el,
  target,
  durationMs
) {

  if (!el) {

    return;

  }


  if (

    prefersReducedMotion

    ||

    target ===
      0

  ) {

    el.textContent =
      target;

    return;

  }


  const start =
    performance.now();


  function tick(
    now
  ) {

    const progress =
      Math.min(

        (
          now -
          start
        )
        /
        durationMs,

        1

      );


    const eased =
      1 -
      Math.pow(
        1 -
        progress,
        3
      );


    el.textContent =
      Math.round(
        eased *
        target
      );


    if (
      progress <
      1
    ) {

      requestAnimationFrame(
        tick
      );

    }

  }


  requestAnimationFrame(
    tick
  );

}


function difficultyFieldHtml() {

  return `

    <div class="field">

      <label for="difficulty-select">
        Difficulty
      </label>


      <select
        class="field-select"
        id="difficulty-select"
      >

        <option
          value="Easy"
          ${
            state.difficulty ===
            "Easy"

              ? "selected"

              : ""
          }
        >
          Easy
        </option>


        <option
          value="Medium"
          ${
            state.difficulty ===
            "Medium"

              ? "selected"

              : ""
          }
        >
          Medium
        </option>


        <option
          value="Hard"
          ${
            state.difficulty ===
            "Hard"

              ? "selected"

              : ""
          }
        >
          Hard
        </option>

      </select>

    </div>

  `;

}


function bindDifficultyField() {

  const select =
    document.getElementById(
      "difficulty-select"
    );


  if (!select) {

    return;

  }


  select.addEventListener(
    "change",
    (
      e
    ) => {


      state.difficulty =
        e.target.value;

    }
  );

}


function loadingHtml(
  message
) {

  return `

    <div class="status-line">

      <span class="spinner"></span>

      ${escapeHtml(
        message
      )}

    </div>

  `;

}


function errorHtml(
  message
) {

  return `

    <div class="status-line is-error">

      ${escapeHtml(
        message
      )}

    </div>

  `;

}


function escapeHtml(
  value
) {

  const div =
    document.createElement(
      "div"
    );


  div.textContent =
    value ?? "";


  return div.innerHTML;

}