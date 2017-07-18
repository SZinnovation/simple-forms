(ns simple-forms-rum.core
  (:require [rum.core :as rum]
            [yaml.core :as yaml]
            [clojure.string :refer [lower-case]])
  (:gen-class))


; should ultimately find a better way to configure the language
; Maybe just load from a config file
(def sz-language "jp")

; This is a little clunky because we're not using keyword maps
; But we're still dispatching on type
(defmulti sz-item #(% "type"))

(defmethod sz-item "vas" 
  [{id "id" 
    ; This documents the expected contents of the map
    {question "question", [left-label right-label] "range_labels"} 
    sz-language}]
  "A simple visual-analog scale component (not a defc'd rum component, though!)"
    [:div {:class "form-group"} 
      [:label {:for id} question]
      [:input {:type "range" :class "not-clicked" :id id :name (lower-case id)
              :min 0 :max 100 :step 1}]
      [:span {:class "ans pull-left"} left-label]
      [:span {:class "ans pull-right"} right-label]
    ]
  )

(defmethod sz-item "instructions"
  [{id "id"
    {instructions "instructions"} sz-language}]
  "A simple div with potentially multi-line instructions"
  [:div instructions]
)

(defmethod sz-item "heading"
  [{id "id"
    {heading "heading"} sz-language}]
  "A simple div with potentially multi-line instructions"
  [:h2 heading]
)

(defmethod sz-item "likert5"
  [{id "id"
    {question "question"} sz-language}]
  "A 5-point likert scale as used in the ADHD self-report scale"
  (let [choices (
        {"en" ["Never" "Rarely" "Sometimes" "Often" "Very Often"],
         "jp" ["全く" "稀に" "たまに" "しばしば" "頻繁に"]} sz-language)]

        ; First we create the static part of our div
        [:div {:class "form-group"} 
          ; Radio buttons have an unusual label approach, so we make our true
          ; label a span for now
          [:div question]
          [:div {:class "row text-center"}
          ; and then we add our choices dynamically
          (into [:div {:class "btn-group" :data-toggle "buttons"}]
            (map-indexed
              (fn [num choice]
                ; For now we're using a bootstrap style
                [:label {:for (str id "-" num) :class "btn btn-primary"}
                  [:input {:type "radio" :id (str id "-" num) :value num :name (lower-case id) 
                            :autocomplete "off"}]
                  choice]
              ) 
              choices) ) ] ]
  ))

(-main "adhd")

(rum/defc sz-form [items]
  "Create a form with some divs"
  ; For now, our containing form tag is in the HTML template
  [:div ;:form
    (keep #(if (% sz-language) (sz-item %)) items)
  ] )

(defn -main
  "Convert a YAML specification into an HTML form"
  [form-name & args]
  (let [form-items (yaml/from-file (format "form-data/%s.yaml" form-name))
        form-html (sz-form form-items)
        template (slurp "form-data/form-template.html")]
    (spit (format "rendered/%s.html" form-name)
      (format template 
        (rum/render-static-markup form-html) ))
  ))

; (-main "vas-gva")