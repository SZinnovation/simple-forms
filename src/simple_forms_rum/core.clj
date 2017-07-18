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
    (if question ; a proxy for "is there data for sz-language?"
      [:div {:class "form-group"} 
        [:label {:for id} question]
        [:input {:type "range" :class "not-clicked" :id id :name (lower-case id)
                :min 0 :max 100 :step 1}]
        [:span {:class "ans pull-left"} left-label]
        [:span {:class "ans pull-right"} right-label]
      ]
    )
  )

(rum/defc sz-form [items]
  "Create a form with some divs"
  ; For now, our containing form tag is in the HTML template
  [:div ;:form
    (keep sz-item items)
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