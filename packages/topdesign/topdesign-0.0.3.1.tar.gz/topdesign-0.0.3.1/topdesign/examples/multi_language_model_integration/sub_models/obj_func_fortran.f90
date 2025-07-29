program obj_func
!  Objective function written in Fortran of 
!  the test problem HS15 from the Hock & Schittkowski collection.
!   min   100 (x2 - x1^2)^2 + (1 - x1)^2
!   s.t.  x1 x2 >= 1
!         x1 + x2^2 >= 0
!         x1 <= 0.5
    implicit none
    real :: x1, x2, obj
    character(len=64) :: arg1, arg2
    integer :: ierror

    ! Check if two arguments are provided
    if (command_argument_count() /= 2) then
        print *, "Please provide two floating-point numbers as arguments."
        stop
    end if

    ! Retrieve the arguments as strings
    call get_command_argument(1, arg1)
    call get_command_argument(2, arg2)

    ! Convert the arguments to real (float) numbers
    read(arg1, *, IOSTAT=ierror) x1
    if (ierror /= 0) then
        print *, "Error reading the first argument as a real number."
        stop
    end if

    read(arg2, *, IOSTAT=ierror) x2
    if (ierror /= 0) then
        print *, "Error reading the second argument as a real number."
        stop
    end if

    ! Calculate the objective function value
    obj = 100 * (x2 - x1**2)**2 + (1 - x1)**2
    
    write(*, *) obj
end program obj_func