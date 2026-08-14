/**
 * mockApi.js
 *
 * Curriculum metadata comes from
 * data/nctb_curriculum_2026.json.
 *
 * No fake chapter fallback is used.
 */


let curriculumCache =
  null;


async function loadCurriculum() {

  if (
    curriculumCache
  ) {

    return curriculumCache;

  }


  const response =
    await fetch(
      "data/nctb_curriculum_2026.json",
      {

        cache:
          "no-store",

      }
    );


  if (
    !response.ok
  ) {

    throw new Error(
      "Missing data/nctb_curriculum_2026.json. Run tools/build_curriculum.py first."
    );

  }


  const data =
    await response.json();


  if (
    data.year !== 2026
  ) {

    throw new Error(
      "The local curriculum file is not marked as NCTB 2026 data."
    );

  }


  curriculumCache =
    data;


  return curriculumCache;

}


function curriculumGradeKey(
  cls
) {

  if (
    cls === "Class 9" ||
    cls === "Class 10"
  ) {

    return "Class 9-10";

  }


  return cls;

}


function chapterLabel(
  chapter
) {

  if (
    typeof chapter === "string"
  ) {

    return chapter;

  }


  const number =
    String(
      chapter?.number ?? ""
    ).trim();


  const title =
    String(
      chapter?.title ?? ""
    ).trim();


  if (!number) {

    return title;

  }


  if (!title) {

    return `অধ্যায় ${number}`;

  }


  const normalizedTitle =
    title.toLocaleLowerCase();


  const normalizedNumber =
    number.toLocaleLowerCase();


  if (

    normalizedTitle.startsWith(
      normalizedNumber
    )

    ||

    normalizedTitle.includes(
      `অধ্যায় ${normalizedNumber}`
    )

    ||

    normalizedTitle.includes(
      `অধ্যায় ${normalizedNumber}`
    )

    ||

    normalizedTitle.includes(
      `chapter ${normalizedNumber}`
    )

  ) {

    return title;

  }


  return `${number}. ${title}`;

}


function samplePassage(
  cls,
  group,
  subject,
  chapter
) {

  const safeSubject =
    String(
      subject || "BOOK"
    );


  return {

    chunk_id:
      `MOCK-${
        safeSubject
          .slice(
            0,
            3
          )
          .toUpperCase()
      }-${
        Math.floor(
          Math.random() *
          900 +
          100
        )
      }`,


    text:
      `[Mock passage] Content from ${chapter} of ${subject} for ${cls}${
        group
          ? `, ${group}`
          : ""
      }.`,


    page:
      Math.floor(
        Math.random() *
        40
      ) + 5,


    score:
      +(
        0.7 +
        Math.random() *
        0.29
      ).toFixed(
        2
      ),

  };

}


let questionCounter =
  1;


const questionStore =
  new Map();


function delay(
  value
) {

  return new Promise(
    (
      resolve
    ) =>

      setTimeout(
        () =>
          resolve(
            value
          ),

        CONFIG.MOCK_LATENCY_MS

      )
  );

}


const MockApi = {


  async getClasses() {

    const data =
      await loadCurriculum();


    return delay({

      classes:
        data.classes,

    });

  },


  async getGroups(
    cls
  ) {

    const data =
      await loadCurriculum();


    return delay({

      class:
        cls,


      groups:
        data
          .groupsByClass?.[
            cls
          ]
        ||
        [],

    });

  },


  async getSubjects(
    cls,
    group = null
  ) {

    const data =
      await loadCurriculum();


    if (

      cls ===
      "Class 9"

      ||

      cls ===
      "Class 10"

    ) {


      if (!group) {

        return delay({

          class:
            cls,

          group:
            null,

          subjects:
            [],

        });

      }


      return delay({

        class:
          cls,


        group,


        subjects:
          data
            .sscSubjectsByGroup?.[
              group
            ]
          ||
          [],

      });

    }


    return delay({

      class:
        cls,


      group:
        null,


      subjects:
        data
          .subjectsByClass?.[
            cls
          ]
        ||
        [],

    });

  },


  async getChapters(
    cls,
    group,
    subject
  ) {

    const data =
      await loadCurriculum();


    const gradeKey =
      curriculumGradeKey(
        cls
      );


    const rawChapters =
      data
        .chapters?.[
          gradeKey
        ]?.[
          subject
        ];


    if (

      !Array.isArray(
        rawChapters
      )

      ||

      rawChapters.length ===
        0

    ) {

      throw new Error(
        `No verified chapter metadata found for ${gradeKey}, ${subject}.`
      );

    }


    return delay({

      class:
        cls,


      group,


      subject,


      chapters:
        rawChapters.map(
          chapterLabel
        ),

    });

  },


  async askQuestion({

    class:
      cls,

    group,

    subject,

    chapter,

    question,

  }) {

    const resolvedChapter =

      chapter ===
      "All Chapters"

        ? "the relevant chapter"

        : chapter;


    const passages = [

      samplePassage(
        cls,
        group,
        subject,
        resolvedChapter
      ),

    ];


    return delay({

      answer:
        `[Mock answer] Based on ${resolvedChapter}, here is a response to: "${question}".`,


      sources:
        passages.map(
          (
            passage
          ) => ({

            chapter:
              resolvedChapter,


            chunk_id:
              passage.chunk_id,

          })
        ),

    });

  },


  async generateMcq({

    class:
      cls,

    group,

    subject,

    chapter,

    difficulty,

  }) {

    const id =
      `mcq_${
        questionCounter++
      }`;


    const correctIndex =
      Math.floor(
        Math.random() *
        4
      );


    const options = [

      "Option A",

      "Option B",

      "Option C",

      "Option D",

    ];


    questionStore.set(
      id,
      {

        type:
          "mcq",


        correctOption:
          options[
            correctIndex
          ],

      }
    );


    return delay({

      question_id:
        id,


      question:
        `[${difficulty}] Sample MCQ generated from ${
          chapter ===
          "All Chapters"

            ? "a random chapter"

            : chapter
        } of ${subject} (${cls})${
          group
            ? `, ${group}`
            : ""
        }.`,


      options,

    });

  },


  async gradeMcq({

    question_id,

    selected_option,

  }) {

    const stored =
      questionStore.get(
        question_id
      );


    if (!stored) {

      throw new Error(
        "Unknown question_id"
      );

    }


    const correct =
      stored.correctOption ===
      selected_option;


    return delay({

      question_id,


      correct,


      correct_option:
        stored.correctOption,


      feedback:
        correct

          ? "Correct."

          : `The correct option was "${stored.correctOption}".`,

    });

  },


  async generateCq({

    class:
      cls,

    group,

    subject,

    chapter,

    difficulty,

  }) {

    const id =
      `cq_${
        questionCounter++
      }`;


    questionStore.set(
      id,
      {

        type:
          "cq",

      }
    );


    return delay({

      question_id:
        id,


      stimulus:
        `[${difficulty}] Sample stimulus generated from ${
          chapter ===
          "All Chapters"

            ? "a random chapter"

            : chapter
        } of ${subject} (${cls})${
          group
            ? `, ${group}`
            : ""
        }.`,


      ka:
        "ক) Placeholder knowledge question.",


      kha:
        "খ) Placeholder comprehension question.",


      ga:
        "গ) Placeholder application question.",


      gha:
        "ঘ) Placeholder higher order question.",

    });

  },


  async gradeCq({

    question_id,

    student_answers,

  }) {

    const stored =
      questionStore.get(
        question_id
      );


    if (!stored) {

      throw new Error(
        "Unknown question_id"
      );

    }


    const parts = [

      "ka",

      "kha",

      "ga",

      "gha",

    ];


    const result =
      {};


    let total =
      0;


    parts.forEach(
      (
        part
      ) => {


        const answered =
          String(
            student_answers[
              part
            ]
            ||
            ""
          )
            .trim()
            .length >
          0;


        const score =
          answered

            ? Math.floor(
                Math.random() *
                3
              ) + 1

            : 0;


        total +=
          score;


        result[
          part
        ] = {

          score,


          feedback:
            answered

              ? "Reasonable attempt."

              : "No answer submitted.",

        };

      }
    );


    result.total =
      total;


    return delay(
      result
    );

  },

};