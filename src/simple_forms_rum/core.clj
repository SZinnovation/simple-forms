(ns simple-forms-rum.core
  (:require [rum.core :as rum]
            [yaml.core :as yaml])
  (:gen-class))


(rum/defc vas-comp [items]
  "Create a form with some divs"
  [:form
    ; At some point we should make language configurable
    ; Right now, we're not guaranteed to have items in all languages
    ; The sensible approach for the demo is to drop those
    (for [item (keep #(% "jp") items)] [:div (item "question")])
  ]
  )

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (let [vas-gva (yaml/from-file "form-data/vas-gva.yaml")
        vas-dom (vas-comp vas-gva)]
  
       (println (rum/render-static-markup vas-dom))
    )
  )

; This gets our working directory
; (System/getProperty "user.dir")