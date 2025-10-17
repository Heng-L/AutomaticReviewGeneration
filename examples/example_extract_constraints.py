"""
Example: Extract constraints from sample text
示例：从样本文本提取约束条件
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from MethodExtraction.ExtractConstraints import (
    extract_constraints_from_literature,
    save_constraints_to_yaml
)

# Sample paper text (模拟的论文文本)
SAMPLE_TEXT = """
Title: Numerical Simulation of Turbulent Flow in a Channel

1. Introduction
This paper presents a numerical study of turbulent flow in a channel using 
computational fluid dynamics (CFD) methods.

2. Numerical Method

2.1 Governing Equations
The incompressible Navier-Stokes equations are solved:

$$\\frac{\\partial u_i}{\\partial t} + u_j \\frac{\\partial u_i}{\\partial x_j} = -\\frac{1}{\\rho}\\frac{\\partial p}{\\partial x_i} + \\nu \\frac{\\partial^2 u_i}{\\partial x_j^2}$$

where $u_i$ is velocity (m/s), $t$ is time (s), $p$ is pressure (Pa), 
$\\rho$ is density (kg/m³), and $\\nu$ is kinematic viscosity (m²/s).

The continuity equation for incompressible flow:

$$\\frac{\\partial u_i}{\\partial x_i} = 0$$

2.2 Boundary Conditions
At the inlet, a uniform velocity profile is prescribed: $u = U_0 = 1.0$ m/s.
At the outlet, a zero gradient boundary condition is applied.
At the walls, no-slip boundary condition is imposed: $u = 0$.

2.3 Discretization
The finite volume method is used for spatial discretization.
The convection terms are discretized using a second-order upwind scheme.
The diffusion terms use central difference scheme.
For time integration, the implicit Euler method is employed with a time step of $\\Delta t = 0.001$ s.

3. Results
[Results section...]
"""

def main():
    print("=" * 60)
    print("示例：提取约束条件")
    print("Example: Extract Constraints")
    print("=" * 60)
    
    # Extract constraints
    print("\n正在提取约束条件...")
    print("Extracting constraints...")
    
    constraints = extract_constraints_from_literature(
        text=SAMPLE_TEXT,
        title="Numerical Simulation of Turbulent Flow in a Channel",
        doi="10.1234/example.2024.001"
    )
    
    # Display results
    print("\n提取结果:")
    print("Extracted results:")
    print("-" * 60)
    
    print("\n1. 元数据 (Metadata):")
    print(f"   标题: {constraints['metadata']['title']}")
    print(f"   DOI: {constraints['metadata']['doi']}")
    
    print("\n2. 控制方程 (Governing Equations):")
    for i, eq in enumerate(constraints['governing_equations'], 1):
        print(f"   方程 {i}: {eq['equation'][:80]}...")
    
    print("\n3. 变量 (Variables):")
    for var in constraints['variables'][:5]:  # Show first 5
        print(f"   {var['symbol']}: {var['description']} ({var['unit']})")
    
    print("\n4. 边界条件 (Boundary Conditions):")
    for bc in constraints['boundary_conditions']['spatial'][:3]:
        print(f"   - {bc[:80]}...")
    
    print("\n5. 离散格式 (Discretization):")
    for scheme in constraints['discretization']['spatial_scheme'][:3]:
        print(f"   - {scheme}")
    
    # Save to YAML
    output_file = "example_constraints.yaml"
    save_constraints_to_yaml(constraints, output_file)
    
    print("\n" + "=" * 60)
    print(f"✓ 完成! 结果保存在: {output_file}")
    print(f"✓ Done! Results saved to: {output_file}")
    print("=" * 60)
    
    # Show YAML content
    print("\nYAML文件内容预览:")
    print("YAML file preview:")
    print("-" * 60)
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content[:500] + "\n...\n")
    
    return constraints


if __name__ == '__main__':
    main()
