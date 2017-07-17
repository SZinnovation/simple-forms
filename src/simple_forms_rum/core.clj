(ns simple-forms-rum.core
  (:require [rum.core :as rum]
            [yaml.core :as yaml]
            [clojure.string :refer [lower-case]])
  (:gen-class))

; This is a little clunky because we're not using keyword maps
(defmulti sz-item #(% "type"))

(defmethod sz-item "vas" 
  [{id "id" 
  ; This documents the expected form-text map
  ; Also, we should find a way to configure the language
   {question "question", [left-label right-label] "range_labels"} "jp"}]
  "A simple visual-analog scale component (not a defc'd rum component, though!)"
      [:div {:class "form-group"} 
        [:label {:for id} question]
        [:input {:type "range" :class "not-clicked" :id id :name (lower-case id)
                 :min 0 :max 100 :step 1}]
        [:span {:class "ans pull-left"} left-label]
        [:span {:class "ans pull-right"} right-label]
      ]
  )

(rum/defc sz-form [items]
  "Create a form with some divs"
  [:form
    ; Convert this to a keep over a multi-method that dispatches on "type"
    (keep sz-item items)
    ; (for [item items
    ;         ; At some point we should make language configurable
    ;         :let [{form-text "jp", id "id"} item]
    ;       ; Right now, we're not guaranteed to have items in all languages
    ;       ; The sensible approach for the demo is to drop those
    ;       :when form-text]
    ;       (vas-input id form-text) )
  ] )

(defn -main
  "Convert a YAML specification into an HTML form"
  [& args]
  (let [vas-gva (yaml/from-file "form-data/vas-gva.yaml")
        vas-dom (sz-form vas-gva)]
    (println (rum/render-static-markup vas-dom))
    )
  )

(-main)

; This gets our working directory
; (System/getProperty "user.dir")