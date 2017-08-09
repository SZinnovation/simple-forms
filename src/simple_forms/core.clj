(ns simple-forms.core
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

(defmethod sz-item "id" [{id "id", label-text sz-language}]
  "A numeric entry field for a student identifier"
  ; It would be nice to do anonymization immediately right here, as well as validation
  [:div {:class "form-group form-inline"}
        [:label {:for id :class "sz-id-label"} label-text]
        [:input {:type "number" :class "form-control" :id id :name (lower-case id)}]
  ] )

(defmethod sz-item "hidden-id" [{id "id"}]
  "A hidden field to auto-populate when we already know the ID somehow" 
  [:input {:type "hidden" :name (lower-case id)}]
  )

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
  [:div instructions [:hr]]
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
         "jp" ["全くない" "めったにない" "たまにある" "よくある" "とてもよくある"]} sz-language)]

        ; First we create the static part of our div
        [:div {:class "form-group"} 
          ; Radio buttons have an unusual label approach, so we make our true
          ; label a span for now
          [:div question]
          [:div {:class "row text-center"}
          ; and then we add our choices dynamically
          (into [:div {:class "btn-group btn-group-sz" :data-toggle "buttons"}]
            (map-indexed
              (fn [num choice]
                ; For now we're using a bootstrap style
                [:label {:for (str id "-" num) :class "btn btn-default"}
                  [:input {:type "radio" :id (str id "-" num) :value num :name (lower-case id) 
                            ; autocomplete fixes "memory" for some browsers on buttons
                            ; http://getbootstrap.com/javascript/#buttons  
                            :autocomplete "off"}]
                  choice]
              ) 
              choices) ) ] ]
  ))

(defmethod sz-item "radio"
  ; Note that radio has very similar structure to likert5 above. Combine?
  [{id "id"
    {question "question",
     choices "choices"} sz-language}]
  (into [:div question]
    (map-indexed
      (fn [num choice]
        ; We're using bootstrap-style nesting of input inside label here to make it easier 
        ; to pack single items into a mapped list
        [:div {:class "radio"}
          [:label {:for (str id "-" num) }
            ; I don't think the autocomlpete issue above is relevant here
            [:input {:type "radio" :id (str id "-" num) :value num :name (lower-case id) }]
            choice]]
      ) 
      choices) ) 
)

(defmethod sz-item "short-answer"
  [{id "id"
    ; Here I'm using a newer style of single-bit-of-text compared to the above
    ; (e.g., likert5 does an extra not-totally-necessary bit of unpacking)
    question sz-language}]
  [:div {:class "form-group"}
    [:label {:for id } question]
    [:br]
    [:input {:type "text" :class "form-control" 
             :id id :name (lower-case id) 
             :autocomplete "off" :inputmode "kana"}]
  ]
)

(rum/defc sz-form [form-name form-data]
  "Create a form with some divs"
  ; For now, our containing form tag is in the HTML template
  (let [[{next-form "next", {button-text sz-language} "button"} & item-data] form-data]
    [:form {:method "post" :action "submissions"}
    [:input {:type "hidden" :name "form-name" :value form-name}]
    [:input {:type "hidden" :name "next-form" :value next-form}]
      ; We only render if there is an entry for our localized data. Can
      ; represent empty with an empty map or string.
      (keep #(if (% sz-language) (sz-item %)) item-data)
      [:button {:type "button submit" :class "btn btn-success btn-lg btn-block"}
        button-text]
    ] ) )

(defn -main
  "Convert a YAML specification into an HTML form"
  [form-name & args]
  (let [form-data (yaml/from-file (format "form-data/%s.yaml" form-name))
        form-html (sz-form form-name form-data)
        template (slurp "form-data/form-template.html")]
    (spit (format "rendered/%s.html" form-name)
      (format template 
        (rum/render-static-markup form-html) ))
  ))