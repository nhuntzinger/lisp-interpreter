; inputs are two lists
; returns a single list that is the two lists concatenated together
(defun append (list1 list2)
    (if (= list1 nil)
        list2
        (append 
            (reverse (cdr (reverse list1)))
            (cons (car (reverse list1)) list2)
            ; This is a comment
        )
    )
)


; input is a list
; output is the list reversed
; in this code, compute the solution on the way back using append
(defun reverseA (list)
    (if (= list nil)
        nil
        (append (reverseA (cdr list)) (cons (car list) nil))
    )
)


; input is a list
; return an integer that counts the number of items in the list
(defun length (list)
    (if (= list nil)
        0
        (+ 1 (length (cdr list)))
    )
)


; input a list of lists
; returns a list of atoms in a preorder traversal of the expression tree
(defun flatten (expr)
    (if (= nil expr)
        nil
        (if (atom expr)
            (cons expr nil)
            (append (flatten (car expr)) (flatten (cdr expr)))
        )
    )
)


; input is two expressions
; return True if the two expressions are the same, False otherwise.
; To be the same they must have the same nested structure and each atom must be eq and in the same position
; Do NOT use flatten to solve this problem
(defun equal (expr0 expr1)
    (if (= nil expr0)
        (if (= nil expr1)
            True
            False
        )
        (if (atom expr0)
            (if (atom expr1)
                (= expr0 expr1)
                False
            )
            (and
                (equal (car expr0) (car expr1))
                (equal (cdr expr0) (cdr expr1))
            )
        )
    )
)


; input is an atom (item) and an expression
; returns True if item is contained anywhere in expression
(defun find (item expr)
    (if (= nil expr)
        False
        (if (= item (car expr))
            True
            (find item (cdr expr))
        )
    )
)


; input is a list and an integer index
; returns the item in the list at index where index 0 is the first of the list
(defun get (list index)
    (getHelp list index 0)
)

(defun getHelp (list index currentIndex)
    (if (= nil list)
        nil
        (if (= currentIndex index)
            (car list)
            (getHelp (cdr list) index (+ 1 currentIndex))
        )
    )
)


; input is a list and two integer indexes of locations within the list. 
; equivalent in Python would be list[start:end]
(defun select (list start end)
    (selectHelpStart list start end 0)
)

(defun selectHelpStart (list start end currentIndex)
    (if (= nil list)
        nil
        (if (= currentIndex start)
            (selectHelpCut list end currentIndex)
            (selectHelpStart (cdr list) start end (+ 1 currentIndex))
        )
    )
)

(defun selectHelpCut (list end currentIndex)
    (if (= nil list)
        nil
        (if (= currentIndex end)
            nil
            (cons (car list) (selectHelpCut (cdr list) end (+ 1 currentIndex)))
        )
    )
)


; takes a list of integers and returns a new list with them sorted in assending order
; int use length and select
(defun mergeSort (list)
    (if (= nil list)
        nil
        (if (= 1 (length list))
            list
            (mergeSortCombine
                (mergeSort (select list 0 (/ (length list) 2)))
                (mergeSort (select list (/ (length list) 2) (length list)))
                nil
            )
        )
    )
)

(defun mergeSortCombine (list1 list2 combined)
    (if (< 0 (length list1))
        (if (< 0 (length list2))
            (if (< (car list1) (car list2))
                (mergeSortCombine (cdr list1) list2 (append combined (cons (car list1) nil)))
                (mergeSortCombine list1 (cdr list2) (append combined (cons (car list2) nil)))
            )
            (append combined list1)
        )
        (append combined list2)
    )
)


; this is a classic dynamic programing problem used in interviews
; given countDice (how many) 6 sided dice and a target (an integer count)
; return the number of ways that the dice may land from a throw such that the top facing numbers on each dice
; add up to target
; Just write the solution recursively.
(defun countThrows (numOfDice target)
    (if (= 0 numOfDice)
        (if (= 0 target) 1 0)

        (if (or (or (< target 0) (or (< (* 6 numOfDice) target) (< numOfDice 0))) (< target numOfDice))
            0
            (sumSixValues
                (countThrows (- numOfDice 1) (- target 1))
                (countThrows (- numOfDice 1) (- target 2))
                (countThrows (- numOfDice 1) (- target 3))
                (countThrows (- numOfDice 1) (- target 4))
                (countThrows (- numOfDice 1) (- target 5))
                (countThrows (- numOfDice 1) (- target 6))
            )
        )
    )
)


; Non-Assignment Methods I wrote
(defun sumSixValues (n1 n2 n3 n4 n5 n6)
    (+ n1 (+ n2 (+ n3 (+ n4 (+ n5 n6)))))
)




; Test Cases

; Append
(append nil (quote (5 8 10 1)))
(append (cons 1 (cons 2 nil )) nil)
(append (quote (1 2 3)) (quote (4 5 6)))

; ReverseA
(reverseA nil)
(reverseA (quote (1 3 7 10 15 3 2 7)))
(reverseA (quote (1 2 3)))
(reverseA (cons 8 (cons 5 (cons 2 nil))))

; Length
(length nil)
(length (cons True (cons False (cons False (cons False nil)))))
(length (quote (1 8 6 4 4 3 2 1)))

; Flatten
(flatten nil )
(flatten 1 )
(flatten (quote (1 2 3 )))
(flatten (quote ((1 )(2 )(3))))
(flatten (quote (1 (7 8 (3)(((4))(5 6))(9 10 0 (11))))))

; Equal
(equal nil nil )
(equal nil 1 )
(equal (quote (1 ))(quote (2 3 4 5 )))
(equal (quote (1 (7 8 (3 )(((4 ))(5 6 ))(9 10 0 (11 )))))(quote (1 (7 8 (3 )(((4 ))(5 6 ))(9 10 0 (11 ))))))
(equal (quote (1 7 8 3)) (quote (1 7 8 3)))

; Find
(find 1 nil)
(find True (cons False (cons False nil)))
(find 111111 (quote (1 2 3 4 6)))
(find 555 (quote (6 555 67 545)))

; Get
(get nil 1)
(get (cons 4 nil) 0)
(get (quote (1 b c d e)) 3)

; select
(select (quote (0 1 2 3 4 5 6 7 8 )) 0 (/ (length (quote (0 1 2 3 4 5 6 7 8 ))) 2 ))
(select (quote (0 1 2 3 4 5 6 7 8 )) (/ (length (quote (0 1 2 3 4 5 6 7 8 ))) 2 )(length (quote (0 1 2 3 4 5 6 7 8 ))))

; Merge Sort
(mergeSort nil )
(mergeSort (quote (1)))
(mergeSort (quote (4 3 1)))
(mergeSort (quote (6 3 2 1 5 7 10)))

; Count Throws
(countThrows 0 0)
(countThrows 1 0)
(countThrows 1 3)
(countThrows 2 7)
(countThrows 2 12)
(countThrows 4 10)
(countThrows 3 16)
(countThrows 3 1)
(countThrows 3 10)
(countThrows 7 6)
