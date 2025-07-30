"
The Hy reader discards line comments.
Here, we implement a Hy model for those comments.
"

(import hy.models [Object String Symbol])
(import hy.reader [HyReader])


(defclass LineComment [Object str]
  "Represent a line comment."

  (defn __new__ [cls [s None]]
    (.__new__ (super) cls (str s)))
    
  (defn __repr__ [self]
    (.__repr__ (super Object self))))



(defclass HyReaderWithLineComments [HyReader]

  (defn [(reader-for ";")] line-comment [self _]
    ;(LineComment (.join "" (self.chars))))))
    None
    #_(let [comment (self.read-chars-until (fn [c] (= c "\n")) "" False)]
        (LineComment comment))))


