;; domain.pddl
(define (domain grid-pathfinding)
    (:requirements :strips :typing)
    (:types location)

    (:predicates
        (at ?loc - location)                        ;; Robot is at ?loc                          
        (connected ?from - location ?to - location) ;; There is a path from ?from to ?to
    )

    (:action move
        :parameters (?from ?to - location)
        :precondition (and 
            (at ?from)
            (connected ?from ?to)
        )
        :effect (and 
            (not (at ?from))
            (at ?to)
        )
    )
)
