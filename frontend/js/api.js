/**
 * api.js
 *
 * Frontend API boundary.
 */

async function realFetch(
  path,
  options = {}
) {

  const res =
    await fetch(
      `${CONFIG.BASE_URL}${path}`,
      {

        headers: {
          "Content-Type":
            "application/json",
        },

        ...options,

      }
    );


  if (!res.ok) {

    const body =
      await res
        .text()
        .catch(
          () => ""
        );


    throw new Error(
      `Request to ${path} failed (${res.status}): ${body}`
    );

  }


  return res.json();

}


const Api = {


  getClasses() {

    return CONFIG.USE_MOCK

      ? MockApi.getClasses()

      : realFetch(
          "/metadata/classes"
        );

  },


  getGroups(
    cls
  ) {

    return CONFIG.USE_MOCK

      ? MockApi.getGroups(
          cls
        )

      : realFetch(
          `/metadata/groups?class=${
            encodeURIComponent(
              cls
            )
          }`
        );

  },


  getSubjects(
    cls,
    group = null
  ) {

    const params =
      new URLSearchParams();


    params.set(
      "class",
      cls
    );


    if (group) {

      params.set(
        "group",
        group
      );

    }


    return CONFIG.USE_MOCK

      ? MockApi.getSubjects(
          cls,
          group
        )

      : realFetch(
          `/metadata/subjects?${params.toString()}`
        );

  },


  getChapters(
    cls,
    group,
    subject
  ) {

    const params =
      new URLSearchParams();


    params.set(
      "class",
      cls
    );


    params.set(
      "subject",
      subject
    );


    if (group) {

      params.set(
        "group",
        group
      );

    }


    return CONFIG.USE_MOCK

      ? MockApi.getChapters(
          cls,
          group,
          subject
        )

      : realFetch(
          `/metadata/chapters?${params.toString()}`
        );

  },


  askQuestion(
    payload
  ) {

    return CONFIG.USE_MOCK

      ? MockApi.askQuestion(
          payload
        )

      : realFetch(
          "/qa",
          {

            method:
              "POST",

            body:
              JSON.stringify(
                payload
              ),

          }
        );

  },


  generateMcq(
    payload
  ) {

    return CONFIG.USE_MOCK

      ? MockApi.generateMcq(
          payload
        )

      : realFetch(
          "/mcq/generate",
          {

            method:
              "POST",

            body:
              JSON.stringify(
                payload
              ),

          }
        );

  },


  gradeMcq(
    payload
  ) {

    return CONFIG.USE_MOCK

      ? MockApi.gradeMcq(
          payload
        )

      : realFetch(
          "/mcq/grade",
          {

            method:
              "POST",

            body:
              JSON.stringify(
                payload
              ),

          }
        );

  },


  generateCq(
    payload
  ) {

    return CONFIG.USE_MOCK

      ? MockApi.generateCq(
          payload
        )

      : realFetch(
          "/cq/generate",
          {

            method:
              "POST",

            body:
              JSON.stringify(
                payload
              ),

          }
        );

  },


  gradeCq(
    payload
  ) {

    return CONFIG.USE_MOCK

      ? MockApi.gradeCq(
          payload
        )

      : realFetch(
          "/cq/grade",
          {

            method:
              "POST",

            body:
              JSON.stringify(
                payload
              ),

          }
        );

  },

};