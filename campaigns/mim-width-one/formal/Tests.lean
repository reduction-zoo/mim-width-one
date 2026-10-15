import Challenge
open MimWidthOne
example : cutWidthOne ⟨4,[(0,2),(1,3),(0,1)]⟩ [0,1] = false := by native_decide
example : cutWidthOne ⟨4,[(0,2),(1,3),(0,3)]⟩ [0,1] = true := by native_decide
example : displays ⟨⟨6,[(0,4),(1,4),(4,5),(2,5),(3,5)]⟩,[0,1,2,3]⟩ ⟨0,1,2,3⟩ = true := by native_decide
example : displays ⟨⟨5,[(0,4),(1,4),(2,4),(3,4)]⟩,[0,1,2,3]⟩ ⟨0,1,2,3⟩ = false := by native_decide
