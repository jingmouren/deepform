import numpy as np
import numpy.ma as ma


def document_edges(tokens, relative_tolerance=0.01):
    """"""

    # For now we compute alignment of text tokens based on their lower left corner.
    dX = np.subtract.outer(tokens["x0"].to_numpy(), tokens["x0"].to_numpy())

    dY = np.subtract.outer(tokens["y1"].to_numpy(), tokens["y1"].to_numpy())

    D = np.abs(dX) + np.abs(dY)
    V_sim = dY / D
    H_sim = dX / D

    dX_h_aligned = ma.masked_where(
        np.logical_not(np.isclose(np.abs(H_sim), 1, rtol=relative_tolerance)), dX
    )
    dY_v_aligned = ma.masked_where(
        np.logical_not(np.isclose(np.abs(V_sim), 1, rtol=relative_tolerance)), dY
    )

    test_right = ma.masked_where(np.greater(dX_h_aligned, 0), dX_h_aligned)
    test_bottom = ma.masked_where(np.greater(dY_v_aligned, 0), dY_v_aligned)

    right_max = np.argmax(test_right, axis=0)
    bottom_max = np.argmax(test_bottom, axis=0)

    adjacency = np.eye(len(tokens))

    for i in range(len(tokens)):
        if dX_h_aligned[i, right_max[i]]:
            adjacency[i, right_max[i]] = 1
            adjacency[right_max[i], i] = 1
        if dY_v_aligned[i, bottom_max[i]]:
            adjacency[i, bottom_max[i]] = 1
            adjacency[bottom_max[i], i] = 1

    return adjacency
