"""Test for config flow"""
from tests.const import CONFIG_DATA
from unittest.mock import patch
import pytest
from homeassistant import config_entries, data_entry_flow, setup
from homeassistant.const import CONF_NAME
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.ncaaf.const import CONF_TEAM_ID, DOMAIN


@pytest.mark.parametrize(
    "input,step_id,title,data",
    [
        (
            {
                "name": "Testing State",
                "team_id": "SEA",
                "timeout": 120,
            },
            "user",
            "Testing State",
            {
                "name": "Testing State",
                "team_id": "SEA",
                "timeout": 120,
            },
        ),
    ],
)
async def test_form(
    input,
    step_id,
    title,
    data,
    hass,
):
    """Test we get the form."""
    await setup.async_setup_component(hass, "persistent_notification", {})
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == "form"
    assert result["errors"] == {}
    # assert result["title"] == title_1

    with patch(
        "custom_components.ncaaf.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], input
        )

        assert result2["type"] == "create_entry"
        assert result2["title"] == title
        assert result2["data"] == data

        await hass.async_block_till_done()
        assert len(mock_setup_entry.mock_calls) == 1


# @pytest.mark.parametrize(
#     "user_input",
#     [
#         {
#             DOMAIN: {
#                 CONF_NAME: "NCAAF",
#                 CONF_TEAM_ID: "SEA",
#             },
#         },
#     ],
# )
# async def test_import(hass, user_input):
#     """Test importing a gateway."""
#     await setup.async_setup_component(hass, "persistent_notification", {})

#     with patch(
#         "custom_components.ncaaf.async_setup_entry",
#         return_value=True,
#     ):
#         result = await hass.config_entries.flow.async_init(
#             DOMAIN, data=user_input, context={"source": config_entries.SOURCE_IMPORT}
#         )
#         await hass.async_block_till_done()

#     assert result["type"] == "create_entry"
