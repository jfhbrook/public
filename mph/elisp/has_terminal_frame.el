(seq-some (lambda (frame)
            (let ((kind (framep frame)))
              (or (eq kind 't )
                  (eq kind 'pc))))
          (frame-list))