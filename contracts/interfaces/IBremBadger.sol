// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.4;

interface IBremBadger {
  error AddressEmptyCode(address target);
  error AddressInsufficientBalance(address account);
  error ERC1967InvalidImplementation(address implementation);
  error ERC1967NonPayable();
  error FailedInnerCall();
  error InvalidInitialization();
  error NotInitializing();
  error ReentrancyGuardReentrantCall();
  error SafeERC20FailedOperation(address token);
  error UUPSUnauthorizedCallContext();
  error UUPSUnsupportedProxiableUUID(bytes32 slot);

  event DepositsDisabled();
  event DepositsEnabled(uint256 start, uint256 end);
  event Initialized(uint64 version);
  event Terminated();
  event Upgraded(address indexed implementation);

  function ADMIN() external view returns (address);
  function DEPOSIT_PERIOD_IN_SECONDS() external view returns (uint256);
  function ONE_WEEK_IN_SECONDS() external view returns (uint256);
  function OWNER() external view returns (address);
  function REM_BADGER_TOKEN() external view returns (address);
  function UNLOCK_TIMESTAMP() external view returns (uint256);
  function UPGRADE_INTERFACE_VERSION() external view returns (string memory);
  function VESTING_WEEKS() external view returns (uint256);
  function deposit(uint256 _amount) external;
  function depositEnd() external view returns (uint256);
  function depositStart() external view returns (uint256);
  function disableDeposits() external;
  function enableDeposits() external;
  function initialize() external;
  function proxiableUUID() external view returns (bytes32);
  function terminate() external;
  function terminated() external view returns (bool);
  function totalClaimed(address) external view returns (uint256);
  function totalDeposited(address) external view returns (uint256);
  function upgradeToAndCall(
    address newImplementation,
    bytes memory data
  ) external payable;
  function vestedAmount(address _depositor) external view returns (uint256);
  function withdrawAll() external;
}
