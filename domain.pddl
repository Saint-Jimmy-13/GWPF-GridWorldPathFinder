;;; ========================================
;;; PDDL Domain: Grid Pathfinding
;;; ========================================
;;;
;;; Domain for solving grid-based pathfinding problems
;;; using automated planning.
;;;
;;; Objects: Locations (cells in a grid)
;;; Predicates:
;;;   - (at ?loc): Robot is currently at location ?loc
;;;   - (connected ?from ?to): There is an adjacent edge from ?from to ?to
;;;
;;; Actions:
;;;   - move(?from, ?to): Move robot from ?from to ?to if they are connected
;;;
(define (domain grid-pathfinding)
    (:requirements :strips :typing)

    (:types location)

    (:predicates
        ;; Current position of the robot
        (at ?loc - location)

        ;; Connectivity between adjacent cells
        ;; This is defined in the problem instance
        (connected ?from - location ?to - location)
    )

    (:action move
        :parameters (?from ?to - location)
        :precondition (and
            ;; Precondition: Robot must be at the source location
            ;;              and there must be an edge to the destination
            (at ?from)
            (connected ?from ?to)
        )
        :effect (and
            ;; Effect: Robot leaves the source location
            ;;         and arrives at the destination
            (not (at ?from))
            (at ?to)
        )
    )
)
