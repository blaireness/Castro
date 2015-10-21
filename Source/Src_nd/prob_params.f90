
! This module stores the runtime parameters that define the problem domain.  
! These parameter are initialized in set_problem_params().

module prob_params_module

  implicit none

  ! boundary condition information
  integer, save :: physbc_lo(3)
  integer, save :: physbc_hi(3)
  integer, save :: Outflow, Symmetry, SlipWall, NoSlipWall

  ! geometry information
  integer         , save :: coord_type
  double precision, save :: center(3), problo(3), probhi(3)

  ! dimension information
  integer         , save :: dim

  ! indices that we use for dimension agnostic routines 
  ! to ensure we don't illegally access non-existent ghost cells
  integer         , save :: dg(3)

  !$acc declare create(physbc_lo, physbc_hi, Outflow, Symmetry, SlipWall, NoSlipWall) &
  !$acc create(coord_type, center, problo, probhi, dim, dg)
  
end module prob_params_module
